from bluetooth import *
import time

port = 1

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",port))
server_sock.listen(1)


print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)

try:
    start = time.time()
    while True:
        data = client_sock.recv(1024)
        if len(data) == 9: break
        print("received [%s]" % data)
        print(time.time()-start)
        start= time.time()
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

