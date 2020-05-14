import re
import time
import math
from collections import deque
from queue import Queue
import threading
import bluetooth


class Animate_phone:

    def __init__(self,client_sock,server_sock):
    
        #Used for reading and handling user inputs
        self.client_sock = client_sock
        self.server_sock = server_sock

        #Default stats label to be displayed
        self.stats = ['Fall Status: False','Fall Distance: Nan']

        #setting up the defaults
        self.azimuth = 0
        self.pitch = 0
        self.roll = 0

        self.vx = 0
        self.vy = 0
        self.vz = 0

        #used to display animation
        self.begin_animation = False

        #exit game condition
        self.animation_data = deque()
        self.display_data = Queue()
        

        self.iter_barrier = threading.Barrier(2)



    def save_and_close_animation_doc(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(''.join([timestr,".txt"]), "w") as output:
            output.write(str(list(self.animation_data)))
        pass
    
    def parse_save_data(self,data,state,s0,s1):
        time = float(data[1])
        temp = data[3:]
        temp = [float(i) for i in temp] 

        self.azimuth = temp[0]
        self.pitch = temp[1]
        self.roll = temp[2]

        self.vx = temp[3]
        self.vy = temp[4]
        self.vz = temp[5]

        self.display_data.put(temp+[s0,s1])
        self.stats[0] = s0
        self.stats[1] = s1

        if state==0:
            self.inital_velocity = temp[3:]
            self.animation_data.clear()
            self.animation_data.append((time,temp[:3]))
            
        elif state==1:
            self.animation_data.append((time,temp[:3]))
        else:
            #begin animation
            self.begin_animation = True
            self.animation_data.append((time,temp[:3]))
        
    def valid_data(self,data):
            return all(not(re.match(r'^-?\d+(?:\.\d+)?$', d) is None) for d in data[3:]) and not(re.match(r'^-?\d+(?:\.\d+)?$', data[1]) is None)

    
    def get_recent_valid_data(self):
        while True:
            data = str(self.client_sock.recv(1024).decode('utf-8'))
            data= data.split(',')
            
            if len(data)== 9 and self.valid_data(data):
                valid = False
                state = 1
                s1 = 'Fall Distance: tbd'
                s0 = 'Fall Status: False'
                save = False

                if data[0]=="~~":
                    s0 = ''.join(['Fall Status: ', str('true' in data[2])])
                    valid = True
                    state = 1

                elif data[0] =="**":
                    s0 = ''.join(['Fall Status: ', str('true' in data[2])])
                    state =0

                elif data[0]=="##":
                    s1 ='Fall Distance: '+data[2]
                    state = 2
                    save =True
                    valid = True

                if valid:
                    self.parse_save_data(data,state,s0,s1)
                    if save:
                        self.save_and_close_animation_doc()

                    self.iter_barrier.wait()
                    self.iter_barrier.wait()
    
    def run(self):
        self.bluetoth_thread = threading.Thread(target=self.get_recent_valid_data)
        self.bluetoth_thread.start()
        start = time.time()
        counter = 0
        while True:
            self.iter_barrier.wait()
            counter +=1
            if counter ==10:
                print("Time for 10 data",time.time()-start)
            print(counter)

            # if not(self.display_data.empty()):
            #     print(self.display_data.get())

            self.iter_barrier.wait()
        
        



    # def update(self,dt):
    #     if  'false' in self.stats[0].lower():
    #             self.scene.bgColor = 138/255, 113/255, 145/255
    #     else:
    #             self.scene.bgColor = 12/255, 100/255, 12/255
        
    #     # if not(self.display_data.empty()):
    #     #         next_up = self.display_data.get()
                
    #     #         self.azimuth = next_up[0]
    #     #         self.pitch = next_up[1]
    #     #         self.roll = next_up[2]

    #     #         self.vx = next_up[3]
    #     #         self.vy = next_up[4]
    #     #         self.vz = next_up[5]

    #     #         self.stats[0] = next_up[6]
    #     #         self.stats[1] = next_up[7]