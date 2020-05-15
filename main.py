from plotter import Plotter
from bluedot.btcomm import BluetoothServer
import re #used to validate states


stats = ['Fall Status: False','Fall Distance: Nan',"Pitch: 0","Roll: 0",'Bluetooth Connected: False']
display_stats = lambda l:'\n'.join(l)
validate_data = lambda data:all(not(re.match(r'^-?\d+(?:\.\d+)?$', d) is None) for d in data[3:]) and not(re.match(r'^-?\d+(?:\.\d+)?$', data[1]) is None)
update= False
begin_animation = False

def data_received(data):
    global begin_animation,stats

    stats[4] = 'Bluetooth Connected: True'

    data= data.split(',')
    print(data[1])
    if len(data)==9 and validate_data(data):
        
        if data[0] !="##":
            stats[0] =''.join(['Fall Status: ', str('true' in data[2])])
        else:
            stats[1] ='Fall Distance: '+data[2]
            begin_animation = True
    
    

s = BluetoothServer(data_received)#starts RFCOMM Server
plot = Plotter(display_stats(stats))
plot.start()



while True:
    # print(stats[4])
    # plot.update_label(display_stats(stats))
    
    pass

s.stop()



