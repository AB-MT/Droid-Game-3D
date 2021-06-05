
# net
# In-game packets
PACKET_SETUP = 0  # Load a new map
PACKET_CONTROLLER = 1  # Controller update
PACKET_SPAWN = 2  # Spawn an entity
PACKET_DELETE = 3  # Delete an entity
PACKET_ENDMATCH = 4  # Sent by the backend
PACKET_NEWCLIENT = 5  # New client is connecting
PACKET_REQUESTSPAWNPACKET = 6  # Client missed a spawn packet
PACKET_DISCONNECT = 7  # Server or client disconnect
PACKET_SERVERFULL = 8  # Server can't take any more clients
PACKET_CHAT = 9  # Chat data
PACKET_EMPTY = 10  # No data. Used for establishing and maintaining connections
PACKET_CLIENTREADY = 11  # Client is done loading
PACKET_ENTITYCHECKSUM = 12  # Packet contains the number of currently active entities
# Client has the wrong number of active entities, so it needs a full list
# of IDs
PACKET_REQUESTENTITYLIST = 13
PACKET_ENTITYLIST = 14  # Packet contains a list of active entity IDs

# For communication with lobby server
PACKET_REQUESTHOSTLIST = 15  # Client requesting the host list from the lobby server
PACKET_HOSTLIST = 16  # Packet contains host list
PACKET_REGISTERHOST = 17  # A host is notifying the lobby server of its existence
# Lobby server notifying the server that a new client wishes to connect
PACKET_NEWCLIENTNOTIFICATION = 18
# Client notifying lobby server of its intention to connect to a host
PACKET_CLIENTCONNECTNOTIFICATION = 19
PACKET_CONFIRMREGISTER = 20  # Lobby server confirms host registration

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

SERVER_TICK = 0.05  # Transfer update packets 20 times per second
