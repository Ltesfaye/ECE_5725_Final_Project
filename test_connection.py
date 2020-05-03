# import bluetooth 
# import json
# import time
# import subprocess
# import os


# # Global Variables
# srcPath = "../data-collector/build/data-collector"
# dirPath = os.path.dirname(os.path.realpath(__file__))
# sendString = ""

# while True:
#     # Define Server Socket on RFCOMM
#     serverSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#     serverSocket.bind(("", bluetooth.PORT_ANY))
#     # Listen on port 1
#     port = serverSocket.getsockname()[1]
#     serverSocket.listen(1)

#     print("listening on port", port)

#     # Advertise Socket
#     uuid = "2f3b0104-fcb0-4bcf-8dda-6b06390c3c1a"
#     bluetooth.advertise_service(serverSocket, "spectral-data-collector", uuid)

#     # Wait for client to connect
#     clientSocket, address = serverSocket.accept()
#     print("Accepted connection from ", address)

import bluetooth

server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = bluetooth.get_available_port( bluetooth.RFCOMM )
server_sock.bind(("",port))
server_sock.listen(1)
print "listening on port %d" % port

uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
bluetooth.advertise_service( server_sock, "FooBar Service", uuid )

client_sock,address = server_sock.accept()
print "Accepted connection from ",address

data = client_sock.recv(1024)
print "received [%s]" % data