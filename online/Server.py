from panda3d.core import * # optimize game
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
from direct.showbase.DirectObject import DirectObject
from direct.task.Task import Task

class Server(QueuedConnectionManager):
	def __init__(self,p,b,username):
		self.cManager = QueuedConnectionManager()
		self.cListener = QueuedConnectionListener(self.cManager, 0)
		self.cReader = QueuedConnectionReader(self.cManager, 0)
		self.cWriter = ConnectionWriter(self.cManager,0)
		self.port = p
		self.backlog = b
		self.socket = self.cManager.openTCPServerRendezvous(self.port,self.backlog)
		self.cListener.addConnection(self.socket)
		
	def tskReaderPolling(self,regClass): 
		if self.cReader.dataAvailable():
			self.datagram=NetDatagram()  
			
			if self.cReader.getData(self.datagram):
				regClass.updateData(self.datagram.getConnection(), self.datagram,self)
					
		return Task.cont
	def tskListenerPolling(self,regClass): 
		if self.cListener.newConnectionAvailable():
			self.rendezvous = PointerToConnection()
			self.netAddress = NetAddress()
			self.newConnection = PointerToConnection()
			if self.cListener.getNewConnection(self.rendezvous,self.netAddress,self.newConnection):
				self.newConnection = self.newConnection.p()
				regClass.PlayerList.append(player(username))
				regClass.PlayerList[regClass.active].connectionID = self.newConnection
				regClass.sendInitialInfo(regClass.active, self)
				regClass.active += 1
				self.cReader.addConnection(self.newConnection)  
		return Task.cont

	
class PlayerReg(DirectObject): 
	def __init__(self):
		self.PlayerList = []
		self.active = 0
		self.timeSinceLastUpdate = 0
		
	
	def updatePlayers(self,serverClass,data,type):
		if (type == "positions"):
			
			self.elapsed = globalClock.getDt()
			self.timeSinceLastUpdate += self.elapsed
			if (self.timeSinceLastUpdate > 0.1):
				if (self.active):
					self.datagram = PyDatagram()
					self.datagram.addString("update")
					
					self.datagram.addFloat64(self.active)
					
					for k in range(self.active):
						self.datagram.addFloat64(self.PlayerList[k].currentPos['x'])
						self.datagram.addFloat64(self.PlayerList[k].currentPos['y'])
						self.datagram.addFloat64(self.PlayerList[k].currentPos['z'])
						self.datagram.addFloat64(self.PlayerList[k].currentPos['h'])
						self.datagram.addFloat64(self.PlayerList[k].currentPos['p'])
						self.datagram.addFloat64(self.PlayerList[k].currentPos['r'])
					for k in self.PlayerList:
						self.conn = k.connectionID
						serverClass.cWriter.send(self.datagram,self.conn)
				self.timeSinceLastUpdate = 0
			return Task.cont
		
		if(type == "chat"):
			
			self.iterator = data
			self.datagram = PyDatagram()
			self.datagram.addString("chat")
			self.text = self.iterator.getString()
			self.datagram.addString(self.text)
			for k in self.PlayerList:
				serverClass.cWriter.send(self.datagram,k.connectionID)
				
				
		
	def updateData(self,connection, datagram,serverClass):
		self.iterator = PyDatagramIterator(datagram)
		self.type = self.iterator.getString()
		if (self.type == "positions"):
			for k in self.PlayerList:
				if (k.connectionID == connection):
					k.currentPos['x'] = self.iterator.getFloat64()
					k.currentPos['y'] = self.iterator.getFloat64()
					k.currentPos['z'] = self.iterator.getFloat64()
					k.currentPos['h'] = self.iterator.getFloat64()
					k.currentPos['p'] = self.iterator.getFloat64()
					k.currentPos['r'] = self.iterator.getFloat64()
		if (self.type == "chat"):
			self.updatePlayers(serverClass,self.iterator,"chat")
	
	def sendInitialInfo(self,i,server): 
		self.con = self.PlayerList[i].connectionID 
		self.datagram = PyDatagram() 
		self.datagram.addString("init") 
		self.datagram.addUint8(self.active) 
		self.datagram.addFloat64(i) 
		for k in self.PlayerList: 
			self.datagram.addString(k.username)
			self.datagram.addFloat64(k.currentPos['x'])
			self.datagram.addFloat64(k.currentPos['y'])
			self.datagram.addFloat64(k.currentPos['z'])
		server.cWriter.send(self.datagram,self.con)

class player(DirectObject):
	def __init__(self, username):
		self.connectionID = 0
		self.username = username
		self.currentPos = {'x':0,'y':0,'z':0,'h':0,'p':0,'r':0} 
		self.isMoving = False
