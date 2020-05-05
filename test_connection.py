# import sys
# import bluetooth

# uuid = "1e0ca4ea-299d-4335-93eb-27fcfe7fa848"
# service_matches = bluetooth.find_service( uuid = uuid )

# if len(service_matches) == 0:
#     print "couldn't find the FooBar service"
#     sys.exit(0)

# first_match = service_matches[0]
# port = first_match["port"]
# name = first_match["name"]
# host = first_match["host"]

# print "connecting to \"%s\" on %s" % (name, host)

# sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
# sock.connect((host, port))
# sock.send("hello!!")
# sock.close()

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

client_sock.close()
server_sock.close()