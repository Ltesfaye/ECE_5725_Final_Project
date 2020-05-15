from plotter import Plotter
from bluedot.btcomm import BluetoothServer
import re #used to validate states
from collections import deque
import threading
import time
import numpy as np

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

for i in range(5):
    cleanser()

stats = ['Fall Status: False','Fall Distance: Nan',"Pitch: 0","Roll: 0",'B-Paired: False']
update= False
begin_animation = False
updated_data=deque()


display_stats = lambda l:'\n'.join(l)
plot = Plotter(display_stats(stats))
plot.start()

def run(event):
    should_kill_thread=False
    def when_client_leaves():
        should_kill_thread= True
    def data_received(data):
        updated_data.append(data) # adds data to the queue and leaves


    s = BluetoothServer(data_received,when_client_disconnects=when_client_leaves)#starts RFCOMM Server

    while True:
        event_set = event.wait(0.00001)
        if event_set or should_kill_thread:
            s.stop()
            break
        pass


e = threading.Event()
if threading.current_thread() is threading.main_thread():
    display_thread = threading.Thread(target=run,args=(e,))
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




initial_velocity=[] 
animation_data=[]
currently_falling=False 

updated_data.clear()
done = False
while not(done) :
        try:
            # st = time.time()
            data = updated_data.popleft()
            stats[4] = 'B-Paired: True'
            data= data.split(',')
            if len(data)==8 and validate_data(data):
                update = True
                stats[2] = "Pitch : "+str(data[3])
                stats[3] = "Roll : "+ str(data[4])
                if data[0] !="##":
                    stats[0] =''.join(['Fall Status: ', str('true' in data[2])])

                    if currently_falling == False and 'true' in data[2]:
                        initial_velocity = data[5:]
                        currently_falling = True
                    
                    if currently_falling == True and not('true' in data[2]):
                        currently_falling = False
                        begin_animation = True
                    
                    if currently_falling:
                        animation_data.append((data[1],data[3:5]))
                        
                else:
                    stats[1] ='Fall Distance: '+data[2]
                    currently_falling = False
                    begin_animation = True
                    e.set() #stop bluetooth thread
            
            if begin_animation:
                plot.update_label(display_stats(stats))
                update=False
                #clearing anything plotted
                plot.reset_pitch_roll_graph()

                animation_data.reverse()
                Dtime, orientation = map(list,zip(*animation_data))
                start_delta_t = Dtime[-1]

                #swapping y and z axis so it looks normal on plot
                vz = initial_velocity[1]
                vx = initial_velocity[0]
                vy = initial_velocity[2]

                x = 0
                y=0
                z=0
                
                while(len(Dtime)>1):
                    new_t = Dtime.pop()
                    Rotations = orientation.pop()

                    time_step = (new_t - start_delta_t)*0.001

                    z += vz*time_step +(0.5)*(9.8)*time_step*time_step 
                    vz -= 9.8*time_step 

                    y += vy*time_step
                    x += vx*time_step

                    plot.add_pitch_value(Rotations[0])
                    plot.add_roll_value(Rotations[1])
                    plot.add_3d_point((x,y,z))
                    start_delta_t = new_t
                
                if len(Dtime)==1:
                    new_t = Dtime.pop()
                    Rotations = orientation.pop()

                    time_step = (new_t - start_delta_t)*0.001

                    z += vz*time_step +(0.5)*(9.8)*time_step*time_step 
                    vz -= 9.8*time_step 

                    y += vy*time_step
                    x += vx*time_step

                    plot.add_pitch_value(Rotations[0])
                    plot.add_roll_value(Rotations[1])
                    plot.add_3d_point((x,y,z),block=True)
                    start_delta_t = new_t


                updated_data.clear() 
                done = True
                pass

            if update:
                plot.update_label(display_stats(stats))
                update=False

            # print(time.time()-st)
        except:
            print("~~~~NO DATA~~~~")
            pass






