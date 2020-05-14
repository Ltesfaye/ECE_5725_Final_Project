import bluetooth

#Setting up the debug flag
debug = False

#setting up bluetooth server socket
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

#waiting for a connection on port1
port=1
server_sock.bind(("",port))
server_sock.listen(1)

