from plotter import Plotter
from bluedot.btcomm import BluetoothServer
import re #used to validate states
from collections import deque
import threading

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
cleanser()
cleanser()

stats = ['Fall Status: False','Fall Distance: Nan',"Pitch: 0","Roll: 0",'B-Paired: False']
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
        for d in range(3,8):
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
updated_data.clear()
while True:
        try:
            data = updated_data.popleft()
            stats[4] = 'B-Paired: True'
            data= data.split(',')
            print(len(data)==8 and validate_data(data))
            if len(data)==8 and validate_data(data):
                update = True
                stats[2] = "Pitch : "+str(data[3])
                stats[3] = "Roll : "+ str(data[4])
                if data[0] !="##":
                    stats[0] =''.join(['Fall Status: ', str('true' in data[2])])

                    if currently_falling == False and 'true' in data[2]:
                        initial_velocity =data[5:]

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
            print("~~~~NO DATA~~~~")
            pass






