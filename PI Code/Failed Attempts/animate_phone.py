import re
import time
import math
import pyglet
import ratcave as rc
from pyglet.window import key
from collections import deque
from queue import Queue
import threading
import bluetooth


# Create window and OpenGL context 
window = pyglet.window.Window(fullscreen=True,visible=True)

# window.set_size(int(700), int(380))


class Animate_phone:

    def __init__(self,client_sock,server_sock):
    
        #Handling user keyboard inputs
        self.keys = key.KeyStateHandler()
        window.push_handlers(self.keys)

        #Used for reading and handling user inputs
        self.client_sock = client_sock
        self.server_sock = server_sock

        #Default stats label to be displayed
        self.stats = ['Fall Status: False','Fall Distance: Nan']

        # Load Meshes and put into a Scene
        obj_reader = rc.WavefrontReader(rc.resources.obj_primitives)
        self.sphere = obj_reader.get_mesh('Sphere', position=(0, 0, -3),scale=0.3)
        self.torus = obj_reader.get_mesh('Torus', position=(0, 0, -3),scale=0.5)
        self.torus2 = obj_reader.get_mesh('Torus', position=(0, 0, -3),scale=0.5)


        #set up diffuse color for meshes
        self.sphere.uniforms['diffuse'] = [.6, .6, .6]
        self.torus.uniforms['diffuse'] = [1, 0, 0]
        self.torus2.uniforms['diffuse'] = [0, 0, 1]

        #setting up the defaults
        self.azimuth = 0
        self.pitch = 0
        self.roll = 0

        self.vx = 0
        self.vy = 0
        self.vz = 0

        #add meshes to scene
        self.scene = rc.Scene(meshes=[self.sphere,self.torus,self.torus2])

        #set up scene background color
        self.scene.bgColor = 138/255, 113/255, 145/255

        #schdules the update and user input functions to run
        pyglet.clock.schedule_interval(self.update, 1.0/40.0)
        # pyglet.clock.schedule_interval(self.get_recent_valid_data, 1.0/60.0)
        pyglet.clock.schedule(self.user_inputs)

        #used to display animation
        self.begin_animation = False

        #exit game condition
        self.end_game=False
        self.animation_data = []
        self.display_data = Queue()
        self.iter_barrier = threading.Barrier(2)



    def save_and_close_animation_doc(self):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        with open(''.join([timestr,".txt"]), "w") as output:
            output.write(str(self.animation_data))
        pass
    
    def parse_save_data(self,data,state,s0,s1):
        time = float(data[1])
        temp = data[3:]
        temp = [float(i) for i in temp] 

        
        # self.display_data.put(temp+[s0,s1])
        self.azimuth = temp[0]
        self.pitch = temp[1]
        self.roll = temp[2]

        self.vx = temp[3]
        self.vy = temp[4]
        self.vz = temp[5]

        self.stats[0] = s0
        self.stats[1] = s1

        if state==0:
            self.inital_velocity = temp[3:]
            self.animation_data=[]
            self.animation_data.append((time,temp[:3]))
            
        elif state==1:
            self.animation_data.append((time,temp[:3]))
        else:
            #begin animation
            self.begin_animation = True
            self.animation_data.append((time,temp[:3]))
        
    def valid_data(self,data):
            return all(not(re.match(r'^-?\d+(?:\.\d+)?$', d) is None) for d in data[3:]) and not(re.match(r'^-?\d+(?:\.\d+)?$', data[1]) is None)

    # Constantly and updating background color
    def update(self,dt):
        if  'false' in self.stats[0].lower():
                self.scene.bgColor = 138/255, 113/255, 145/255
        else:
                self.scene.bgColor = 12/255, 100/255, 12/255
        
    def get_recent_valid_data(self,dt):

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
        
    # Constantly checks for new user inputs and processes it accordingly
    def user_inputs(self,dt):
        if self.keys[key.R]:
            #reset Everything 
            self.torus.rotation.y = 0
            self.torus2.rotation.x = 90
            self.stats = ['Fall Status: False','Fall Distance: Nan']

        if self.keys[key.ESCAPE]:
            #quiting the display
            self.end_game= True

    def run(self):
        # pyglet draw loop
        @window.event
        def on_draw():
            self.torus2.rotation.x = 90
            self.torus.rotation.y = self.roll
            self.torus2.rotation.y = self.pitch

    
            with rc.default_shader:
                self.scene.draw()

            for i in range(len(self.stats)):
                # printing out read in stats loop
                label = pyglet.text.Label(self.stats[i],
                                font_name='Times New Roman',
                                font_size=12,
                                x=10, y=window.height//2-window.height//3 -20*i,
                                anchor_x='left', anchor_y='center')
                label.draw()

            if self.end_game == True:
                self.client_sock.close()
                self.server_sock.close()
                pyglet.app.EventLoop().exit()

        pyglet.app.run() 

    
      
        




