from bluetooth_reciever import launch_program


def cleanser():
    import bluetooth

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

def clean():
    #Resets the bluetooth connection 5 times to clear any buffering issue on pi
    for i in range(5):
        cleanser()

cleanser()
launch_program()