from plotter import Plotter
from bluedot.btcomm import BluetoothServer
import re #used to validate states
from queue import Queue
import threading



stats = ['Fall Status: False','Fall Distance: Nan',"Pitch: 0","Roll: 0",'Bluetooth Connected: False']
update= False
begin_animation = False
updated_data=Queue()


display_stats = lambda l:'\n'.join(l)
plot = Plotter(display_stats(stats))
plot.start()

def run():
    global updated_data

    def data_received(data):
        global updated_data
        stats[4] = 'Bluetooth Connected: True'
        updated_data.put(data) # adds data to the queue and leaves

    s = BluetoothServer(data_received)#starts RFCOMM Server

    while True:
        pass

display_thread = threading.Thread(target=run)
display_thread.start()


def validate_data(data):
    if data[0] in ['~~','##','**']:
        for d in range(3,9):
            try:
                data[d] = float(data[d])
            except:
                return False
        try:
            data[1] = float(data[1])
        except:
            return False
        
        return True
   
    return False



    
        
while True:
        if not(updated_data.empty()):
            data = updated_data.get()
            data= data.split(',')
            if len(data)==9 and validate_data(data):
                print(data[1])
                update = True
                stats[2] = "Pitch : "+str(data[4])
                stats[3] = "Roll : "+ str(data[5])
                if data[0] !="##":
                    stats[0] =''.join(['Fall Status: ', str('true' in data[2])])
                else:
                    stats[1] ='Fall Distance: '+data[2]
                    begin_animation = True
            if update:
                plot.update_label(display_stats(stats))
                update=False






