# import bluetooth
# import time



# #setting up bluetooth server socket
# server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# #waiting for a connection on port1
# port=1
# server_sock.bind(("",port))
# server_sock.listen(1)

# client_sock,address = server_sock.accept()
# print ("Resetting connection from", address)

# client_sock.close()
# server_sock.close()

# time.sleep(1)

# #setting up bluetooth server socket
# server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# #waiting for a connection on port1
# port=1
# server_sock.bind(("",port))
# server_sock.listen(1)
# client_sock,address = server_sock.accept()

# client_sock.settimeout(0.5)

# print ("Accepted connection from", address)
# start = time.time()
# while True:
#     try:
#         data = client_sock.recv(1024)
#         print ("received [%s]" %data)

#         print("Killing it",time.time()-start)
#         start = time.time()

#         if (data=="e"):
#             print("Exit")
#             break
#     except:
#         print("---------Timed Out---------")

    

   

# client_sock.close()
# server_sock.close()


from bluetooth import *

port = 1

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",port))
server_sock.listen(1)


print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data)
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

