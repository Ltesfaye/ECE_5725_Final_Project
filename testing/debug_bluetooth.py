import bluetooth
import time



#setting up bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#waiting for a connection on port1
port=1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()
print ("Resetting connection from", address)

client_sock.close()
server_sock.close()

time.sleep(1)

#setting up bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#waiting for a connection on port1
port=1
server_sock.bind(("",port))
server_sock.listen(1)
client_sock,address = server_sock.accept()

client_sock.settimeout(1)

print ("Accepted connection from", address)
start = time.time()
while True:
   
    data = client_sock.recv(1024)

    print ("received [%s]" %data)

    print("Killing it",time.time()-start)
    start = time.time()

    if (data=="e"):
        print("Exit")
        break

client_sock.close()
server_sock.close()


