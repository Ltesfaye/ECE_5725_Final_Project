from plotter import Plotter
from bluedot.btcomm import BluetoothServer
import re #used to validate states
from collections import deque
import threading



stats = ['Fall Status: False','Fall Distance: Nan',"Pitch: 0","Roll: 0",'Bluetooth Connected: False']
update= False
begin_animation = False
updated_data=deque()


display_stats = lambda l:'\n'.join(l)
plot = Plotter(display_stats(stats))
plot.start()

def run():
    def data_received(data):
        updated_data.append(data) # adds data to the queue and leaves

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



    
initial_velocity = []  
currently_falling=False 
Fall_initial = [0,0,0]
while True:
        try:
            data = updated_data.popleft()
            stats[4] = 'Bluetooth Connected: True'
            data= data.split(',')
            if len(data)==9 and validate_data(data):
                update = True
                stats[2] = "Pitch : "+str(data[4])
                stats[3] = "Roll : "+ str(data[5])
                if data[0] !="##":
                    stats[0] =''.join(['Fall Status: ', str('true' in data[2])])

                    if currently_falling == False and 'true' in data[2]:
                        initial_velocity =data[6:]

                else:
                    stats[1] ='Fall Distance: '+data[2]
                    currently_falling = False
                    begin_animation = True
            
            if begin_animation:
                updated_data 
                pass

            if update:
                plot.update_label(display_stats(stats))
                update=False
        except:
            pass






