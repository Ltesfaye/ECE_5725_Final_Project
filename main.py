import bluetooth
import signal
import sys
import time





#Setting up the debug flag
debug = False

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

print ("Accepted connection from", address)

#Signal Handler for not safe closing
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    client_sock.close()
    server_sock.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if debug:
    while True:
        data = client_sock.recv(1024)
        print ("received [%s]" %data)

        if (data=="e"):
            print("Exit")
            break
else:
    print("____Starting Display____")
    from parse_bluetooth import Animate_phone
    display = Animate_phone(client_sock,server_sock)
    display.run()


    
