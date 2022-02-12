# ВНИМАНИЕ!
# Английские комментарии из-за того, что это тутоориал по онлайну.

import pyximport # импоритурем Cython
pyximport.install() # инициализируем его
import socket
import time
import zlib
from . import ipgetter
import sys

from . import constants

from direct.distributed.PyDatagram import PyDatagram

netMode = 0

connection = None
initialized = False
context = None

# In-game packets
PACKET_SETUP = 0 # Load a new map
PACKET_CONTROLLER = 1 # Controller update
PACKET_SPAWN = 2 # Spawn an entity
PACKET_DELETE = 3 # Delete an entity
PACKET_ENDMATCH = 4 # Sent by the backend
PACKET_NEWCLIENT = 5 # New client is connecting
PACKET_REQUESTSPAWNPACKET = 6 # Client missed a spawn packet
PACKET_DISCONNECT = 7 # Server or client disconnect
PACKET_SERVERFULL = 8 # Server can't take any more clients
PACKET_CHAT = 9 # Chat data
PACKET_EMPTY = 10 # No data. Used for establishing and maintaining connections
PACKET_CLIENTREADY = 11 # Client is done loading
PACKET_ENTITYCHECKSUM = 12 # Packet contains the number of currently active entities
PACKET_REQUESTENTITYLIST = 13 # Client has the wrong number of active entities, so it needs a full list of IDs
PACKET_ENTITYLIST = 14 # Packet contains a list of active entity IDs

# For communication with lobby server
PACKET_REQUESTHOSTLIST = 15 # Client requesting the host list from the lobby server
PACKET_HOSTLIST = 16 # Packet contains host list
PACKET_REGISTERHOST = 17 # A host is notifying the lobby server of its existence
PACKET_NEWCLIENTNOTIFICATION = 18 # Lobby server notifying the server that a new client wishes to connect
PACKET_CLIENTCONNECTNOTIFICATION = 19 # Client notifying lobby server of its intention to connect to a host
PACKET_CONFIRMREGISTER = 20 # Lobby server confirms host registration

# Spawn types
SPAWN_PLAYER = 0
SPAWN_BOT = 1
SPAWN_PHYSICSENTITY = 2
SPAWN_GRENADE = 3
SPAWN_SPRINGBOARD = 4
SPAWN_GLASS = 5
SPAWN_TEAMENTITY = 6
SPAWN_MOLOTOV = 7
SPAWN_POD = 8

MODE_SERVER = 0
MODE_CLIENT = 1

SERVER_TICK = 0.03 # Transfer update packets 20 times per second

if sys.platform == "win32":
	timeFunction = time.clock
else:
	timeFunction = time.time

def init(localPort=None):
    global context, initialized
    context = PythonNetContext(localPort)
    initialized = True


class NetworkContext:
    def __init__(self, arg, mode, localClientPort=None):
        pass
        # In client mode, arg is the address of the host to connect to.
        # In server mode, arg is the port to listen on.
        # If arg is None, the network thread does nothing.

    def readWorker(self):
        # To be called once inside a daemon thread. Reads packets into a queue.
        pass

    def writeWorker(self):
        # To be called once inside a daemon thread. Writes packets from a queue
        # onto the network interface.
        pass

    def readTick(self):
        pass  # Called in a loop.

    def writeTick(self):
        pass  # Called in a loop.

    def delete(self):
        pass  # Clean up.


class Connection:

    def __init__(self):
        self.address = ("", 0)
        self.lastPacketTime = time.time()
        self.lastSentPacketTime = 0
        self.ready = False


class PythonNetContext(NetworkContext):

    def __init__(self, localPort=None):
        global netMode
        netMode = constants.MODE_SERVER
        self.mode = constants.MODE_SERVER
        if localPort is None:
            localPort = 1337

        self.port = localPort
        self.publicAddress = ipgetter.myip()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.socket.setblocking(False)
        self.bindSocket(localPort)
        self.clientConnected = False
        self.activeConnections = dict()  # Server only - connected clients
        self.hostConnection = Connection()  # Client only - connection to server
        self.writeQueue = []
        self.hostListCallback = None
        self.disconnectCallback = None
        self.connectionTimeout = 10.0 if netMode == constants.MODE_SERVER else 15.0
        self.clientUsername = "Unnamed"
        self.lastConnectionAttempt = 0
        self.connectionAttempts = 0

    def connectToServer(self, arg, username):
        global netMode
        netMode = MODE_CLIENT
        self.mode = MODE_CLIENT
        args = arg.split(":")
        ip = args[0]
        port = 1337
        if len(args) > 1:
            port = int(args[1])

        self.hostConnection.address = (str(ip), port)
        self.hostConnection.lastSentPacketTime = time.time()
        self.hostConnection.ready = True
        self.clientConnected = False
        self.clientUsername = username

    def listen(self):
        global netMode
        netMode = constants.MODE_SERVER
        self.mode = constants.MODE_SERVER

    def reset(self):
        global netMode
        netMode = constants.MODE_SERVER
        self.mode = constants.MODE_SERVER
        self.clientConnected = False
        self.activeConnections.clear()
        self.hostConnection = Connection()
        self.connectionAttempts = 0

    def bindSocket(self, port):
        bound = False
        tries = 0
        while not bound and tries < 10:
            try:
                self.socket.bind(('0.0.0.0', port))
                bound = True
            except BaseException:
                time.sleep(0.25)

            tries += 1

    def clientConnect(self, username):
        if self.clientConnected:
            return

        data = PyDatagram()
        p = Packet()
        p.add(Uint8(constants.PACKET_NEWCLIENT))
        p.add(String(username))
        p.addTo(data)
        self.sendDatagram(data, self.hostConnection.address)
        self.hostConnection.lastSentPacketTime = time.time()

    def serverConnect(self, clientAddress):
        if clientAddress in self.activeConnections:
            return

        data = PyDatagram()
        p = Packet()
        p.add(Uint8(constants.PACKET_EMPTY))
        p.addTo(data)
        self.sendDatagram(data, clientAddress)

    def removeClient(self, client):
        if client in self.activeConnections:
            del self.activeConnections[client]

    def addClient(self, client):
        if client not in self.activeConnections:
            connection = Connection()
            connection.address = client
            connection.lastSentPacketTime = time.time()
            self.activeConnections[client] = connection

    def resetConnectionStatuses(self):
        for connection in list(self.activeConnections.values()):
            connection.ready = False

    def writeTick(self):
        for data in self.writeQueue:
            # data[0] = action code. 0 for broadcast or broadcastExcept. 1 for send.
            # for broadcasting, the given connection is excluded, if one is given.
            # for sending, the given connection is the only one we send the
            # data to.
            compressedData = zlib.compress(bytes(data[1]))
            if data[0] == 0:  # Broadcast
                for c in (
                        x for x in list(self.activeConnections.values()) if x.ready):
                    c.lastSentPacketTime = time.time()
                    try:
                        self.socket.sendto(compressedData, c.address)
                    except socket.error:
                        pass
            elif data[0] == 1:  # Send to specific machine
                try:
                    self.socket.sendto(compressedData, data[2])
                except socket.error:
                    pass
                if data[2] in self.activeConnections:
                    self.activeConnections[data[2]
                                           ].lastSentPacketTime = time.time()
                elif compareAddresses(data[2], self.hostConnection.address):
                    self.hostConnection.lastSentPacketTime = time.time()
            elif data[0] == 2:  # Broadcast, excluding one machine
                for c in (
                    x for x in list(self.activeConnections.values()) if x.ready and not compareAddresses(
                        x.address,
                        data[2])):
                    try:
                        self.socket.sendto(compressedData, c.address)
                    except socket.error:
                        pass
                    c.lastSentPacketTime = time.time()
        del self.writeQueue[:]

    def readTick(self):
        if self.mode == constants.MODE_SERVER:
            loadingTimeout = self.connectionTimeout * 2
            for client in list(self.activeConnections.values()):
                if time.time() - client.lastPacketTime > (
                        self.connectionTimeout if client.ready else loadingTimeout):
                    del self.activeConnections[client.address]
                    if self.disconnectCallback is not None:
                        self.disconnectCallback(client.address)
        elif self.mode == MODE_CLIENT:
            if self.clientConnected:
                if self.disconnectCallback is not None and time.time(
                ) - self.hostConnection.lastPacketTime > self.connectionTimeout:
                    self.disconnectCallback(self.hostConnection.address)
                    self.clientConnected = False
            else:
                if self.connectionAttempts < 10:
                    if time.time() - self.lastConnectionAttempt > 0.5:
                        self.clientConnect(self.clientUsername)
                        self.connectionAttempts += 1
                        self.lastConnectionAttempt = time.time()
                else:
                    self.connectionAttempts = 0
                    self.disconnectCallback(self.hostConnection.address)

        readQueue = []
        while True:
            try:
                message, address = self.socket.recvfrom(1024)
            except socket.error:
                return readQueue
            
            if not message:
                continue
            
            if address in self.activeConnections:
                self.activeConnections[address].lastPacketTime = time.time()
            
            try:
                message = zlib.decompress(message)
            except zlib.error:
                continue
            
            iterator = PyDatagram(message)
            
            code = Uint8.getFrom(iterator)
            if code == constants.PACKET_HOSTLIST:
                numHosts = Uint16.getFrom(iterator)
                hosts = []
                for _ in range(numHosts):
                    ip = String.getFrom(iterator)
                    port = Uint16.getFrom(iterator)
                    user = String.getFrom(iterator)
                    map = String.getFrom(iterator)
                    activePlayers = Uint8.getFrom(iterator)
                    playerSlots = Uint8.getFrom(iterator)
                    hosts.append((user, map, ip + ":" + str(port),
                                  activePlayers, playerSlots))
                #engine.log.debug("Received " + str(numHosts) + " hosts from lobby server.")
                if self.hostListCallback is not None:
                    self.hostListCallback(hosts)
            if self.mode == constants.MODE_SERVER:
                if code == constants.PACKET_NEWCLIENTNOTIFICATION:
                    ip = String.getFrom(iterator)
                    port = Uint16.getFrom(iterator)
                    clientAddress = (ip, port)
                    self.connectionAttempts = 0
                    #engine.log.info("Received notification from lobby server of new client " + ip + ":" + str(port))
                    self.serverConnect(clientAddress)
                elif code == constants.PACKET_DISCONNECT:
                    if address in self.activeConnections:
                        del self.activeConnections[address]
                elif code == constants.PACKET_CLIENTREADY:
                    if address in self.activeConnections:
                        self.activeConnections[address].ready = True
            elif self.mode == MODE_CLIENT and address == self.hostConnection.address:
                self.hostConnection.lastPacketTime = time.time()
            readQueue.append((message, address))
        return readQueue

    def broadcastDatagram(self, datagram):
        """For the server, broadcasts the given data packet to all connected clients.
        For clients, sends the datagram to the server."""
        if netMode == constants.MODE_SERVER:
            self.writeQueue.append((0, datagram, None))  # Send to all clients
        else:
            self.writeQueue.append(
                (1, datagram, self.hostConnection.address))  # Send to host

    def broadcastDatagramExcept(self, datagram, client):
        """For the server, broadcasts the given data packet to all connected clients.
        For clients, sends the datagram to the server."""
        self.writeQueue.append((2, datagram, client))

    def sendDatagram(self, datagram, client=None):
        self.writeQueue.append((1, datagram, client))

    def broadcast(self, packet):
        d = PyDatagram()
        packet.addTo(d)
        self.broadcastDatagram(d)

    def broadcastExcept(self, packet, client):
        d = PyDatagram()
        packet.addTo(d)
        self.broadcastDatagramExcept(d, client)

    def send(self, packet, client=None):
        d = PyDatagram()
        packet.addTo(d)
        self.sendDatagram(d, client)

    def delete(self):
        p = Packet()
        p.add(Uint8(constants.PACKET_DISCONNECT))
        data = PyDatagram()
        p.addTo(data)
        self.broadcastDatagram(data)
        self.writeTick()
        time.sleep(0.25)
        self.socket.close()


def delete():
    global initialized, context
    initialized = False
    context.delete()


def stringToAddress(string):
    address = string.split(":")
    return (address[0], int(address[1]))


def addressToString(address):
    return address[0] + ":" + str(address[1])


def compareAddresses(a, b):
    return a[0] == b[0] and a[1] == b[1]


def copyAddress(a):
    return (a[0], a[1])


def isValidIp(addressString):
    try:
        addressParts = addressString.split(":")
        ip = addressParts[0]
        if len(addressParts) > 1:
            port = addressParts[1]
            if not 0 <= int(port) <= 2**16:
                return False

        parts = ip.split(".")
        if len(parts) != 4:
            return False

        for item in parts:
            if not 0 <= int(item) <= 255:
                return False
    except BaseException:
        return False

    return True


class Packet:

    def __init__(self):
        self.dataObjects = []

    def getSize(self):
        return len(self.dataObjects)

    def add(self, dataObject):
        assert isinstance(dataObject, NetObject) or isinstance(dataObject, Packet)
        if dataObject is not None:
            self.dataObjects.append(dataObject)

    def addTo(self, datagram):
        for dataObject in self.dataObjects:
            dataObject.addTo(datagram)


def clamp(a, min, max):
    if min <= a <= max:
        return a

    if a < min:
        return min

    return max


class NetObject:
    data = None

    def __init__(self, data):
        self.data = data

    def addTo(self, datagram):
        pass

    @staticmethod
    def getFrom(iterator):
        pass


class HighResFloat(NetObject):

    def addTo(self, datagram):
        datagram.addFloat32(float(self.data))

    @staticmethod
    def getFrom(iterator):
        return iterator.getFloat32()


class StandardFloat(NetObject):

    def addTo(self, datagram):
        datagram.addInt16(clamp(int(self.data * 110.0), -32768, 32767))

    @staticmethod
    def getFrom(iterator):
        return float(iterator.getInt16()) / 110.0


class LowResFloat(NetObject):

    def addTo(self, datagram):
        datagram.addInt16(clamp(int(self.data * 50.0), -32768, 32767))

    @staticmethod
    def getFrom(iterator):
        return float(iterator.getInt16()) / 50.0


class SmallFloat(NetObject):

    def addTo(self, datagram):
        datagram.addInt8(clamp(int(self.data * (127.0 / 35.0)), -128, 127))

    @staticmethod
    def getFrom(iterator):
        return float(iterator.getInt8()) * (35.0 / 127.0)


class Uint8(NetObject):

    def addTo(self, datagram):
        datagram.addUint8(int(self.data))

    @staticmethod
    def getFrom(iterator):
        return iterator.getUint8()


class Uint16(NetObject):

    def addTo(self, datagram):
        datagram.addUint16(int(self.data))

    @staticmethod
    def getFrom(iterator):
        return iterator.getUint16()


class Uint32(NetObject):

    def addTo(self, datagram):
        datagram.addUint32(int(self.data))

    @staticmethod
    def getFrom(iterator):
        return iterator.getUint32()


class Int16(NetObject):

    def addTo(self, datagram):
        datagram.addInt16(int(self.data))

    @staticmethod
    def getFrom(iterator):
        return iterator.getInt16()


class String(NetObject):

    def addTo(self, datagram):
        datagram.addString(str(self.data))

    @staticmethod
    def getFrom(iterator):
        return iterator.getString()


class Boolean(NetObject):

    def addTo(self, datagram):
        datagram.addBool(bool(self.data))

    @staticmethod
    def getFrom(iterator):
        return iterator.getBool()
