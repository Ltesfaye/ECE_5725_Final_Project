from plotter import Plotter # used to plot and animate things
from multiprocessing import Process, Pipe,Event # used to launch python process on separate core
from bluedot.btcomm import BluetoothServer #start bluetooth server to allow phone to connect

def bluetooth_client(conn,done_event):
    
    def data_received(data):
        conn.send(data) # adds data to the queue and leaves

    s = BluetoothServer(data_received)#starts RFCOMM Server
    
    # running = True # used to terminate this process

    while not(done_event.wait(0.00001)):
        pass
       
    conn.close()
    s.stop()
           
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

def launch_run_display(done_event,conn):
    stats = ['Fall Status: False',"Pitch: 0","Roll: 0"]
    update= False
    begin_animation = False

    #used for displaying data on matplotlib
    display_stats = lambda l:'\n'.join(l)
    plot = Plotter(display_stats(stats))
    plot.start()
    plot.draw()

    initial_velocity=[] 
    animation_data=[]
    currently_falling=False 
    
 
    while True:
        data = conn.recv()
        if data.strip(' ')== 'e':
                #case where phone application is shutdown
                done_event.set()
                return
        else:
            data= data.split(',')
            if (len(data)==8 and validate_data(data)):
                update = True
                stats[1] = ''.join(["Pitch : ",str(data[3])])
                stats[2] = ''.join(["Roll : ", str(data[4])])
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
                    # stats[1] = ''.join(['Fall Distance: ',data[2]])
                    currently_falling = False
                    begin_animation = True
                    
            
            if begin_animation:
                print("Killing Bluetooth Process")
                done_event.set() #stop bluetooth process
                
                
                print("~~~starting animation~~~")
                animation_data.reverse()
                Dtime, orientation = map(list,zip(*animation_data))
                start_delta_t = Dtime[-1]

                #swapping y and z axis so it looks normal on plot
                vz = initial_velocity[1]
                vx = initial_velocity[0]
                vy = initial_velocity[2]

                # intial positions
                x=0
                y=0
                z=0
                
                while(len(Dtime)>1):
                    new_t = Dtime.pop()
                    Rotations = orientation.pop()

                    time_step = (new_t - start_delta_t)*0.001

                    z += vz*time_step +(0.5)*(-9.8)*time_step*time_step 
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

                return #kills this function
                

            if update and not(done):
                plot.update_label(display_stats(stats))
                update=False
    
def launch_program():
    quit_event = Event()
    parent_conn, child_conn = Pipe()
    p = Process(target=bluetooth_client, args=(child_conn,quit_event))
    print("Starting Bluetooth Process")
    p.start()
    print("----starting display----")
    launch_run_display(quit_event,parent_conn)
    p.join()# Wait for the bluetooth process  to finish
    print("Exited Safely")

