import bluetooth

#Setting up the debug flag
debug = False

#setting up bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#waiting for a connection on port1
port=1
server_sock.bind(("",port))
server_sock.listen(1)

client_sock,address = server_sock.accept()

print ("Accepted connection from", address)
if debug:
    while True:
        data = client_sock.recv(1024)
        print ("received [%s]" %data)

        if (data=="e"):
            print("Exit")
            break
else:
    print("____Starting Display____")
    from animate_phone import Animate_phone
    display = Animate_phone(client_sock,server_sock)
    display.run()


    
client_sock.close()
server_sock.close()