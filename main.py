from parse_bluetooth import *
from bluetooth import *
import sys,signal

port = 1

server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",port))
server_sock.listen(1)


print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


#Signal Handler for not safe closing
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    client_sock.close()
    server_sock.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

try:
    while True:
        parser_display = Animate_phone(client_sock)
        parser_display.run(debug=True)
        # data = client_sock.recv(1024)
        # if len(data) == 9: 
        #     print("received [%s]" % data)
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

