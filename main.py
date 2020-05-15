from parse_bluetooth import *
from bluetooth import *


port = 1
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",port))
server_sock.listen(1)


print("Waiting for connection on RFCOMM channel %d" % port)
client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)


try:
    stats = ['Fall Status: False','Fall Distance: Nan',"Pitch :0","Roll:0"]
    display_stats = lambda l:'\n'.join(l)
    plot = Plotter(display_stats(stats))
    plot.start()
    while True:
        data = str(client_sock.recv(1024).decode('utf-8'))
        data= data.split(',')
        if len(data) == 9: 
            print("received [%s]" % data[0])
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")

