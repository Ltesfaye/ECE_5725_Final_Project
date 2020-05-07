
import pyglet
import ratcave as rc
from pyglet.window import key
import time
import math
import bluetooth

# from shader import vert_shader,frag_shader
# shader = rc.Shader(vert=vert_shader, frag=frag_shader)
# Create window and OpenGL context 
window = pyglet.window.Window()

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

        #add meshes to scene
        self.scene = rc.Scene(meshes=[self.sphere,self.torus,self.torus2])

        #set up scene background color
        self.scene.bgColor = 138/255, 113/255, 145/255

        #schdules the update and user input functions to run
        pyglet.clock.schedule(self.update)
        pyglet.clock.schedule(self.user_inputs)

        #exit game condition
        self.end_game=False


    # Constantly-Running mesh rotation, for fun
    def update(self,dt):
        self.torus.rotation.y += 40. * dt
    

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
        # Pyglet's event loop run function
        # Draw Function
        @window.event
        def on_draw():
            data = self.client_sock.recv(1024)
            print ("received [%s]" %data)
            self.torus2.rotation.x = 90
            
            if self.stats[0] =='Fall Status: False':
                self.scene.bgColor = 138/255, 113/255, 145/255
            else:
                self.scene.bgColor = 12/255, 100/255, 12/255
            


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
        pass




