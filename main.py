from plotter import Plotter
from bluedot.btcomm import BluetoothServer


stats = ['Fall Status: False','Fall Distance: Nan',"Pitch :0","Roll:0"]
display_stats = lambda l:'\n'.join(l)

def data_received(data):
    print(data)
    

s = BluetoothServer(data_received)#starts RFCOMM Server

plot = Plotter(display_stats(stats))

while True:
    
    pass

s.stop()



