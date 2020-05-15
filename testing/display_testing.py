from bluedot.btcomm import BluetoothServer
from signal import pause

def data_received(data):
    print(data)
    

s = BluetoothServer(data_received)
pause()




# import pyglet
# import ratcave as rc
# from pyglet.window import key
# import time
# import math


# # Create window and OpenGL context (always must come first!)
# window = pyglet.window.Window(resizable=True)
# keys = key.KeyStateHandler()
# window.push_handlers(keys)


# # Load Meshes and put into a Scene
# obj_reader = rc.WavefrontReader(rc.resources.obj_primitives)
# sphere = obj_reader.get_mesh('Sphere', position=(0, 0, -3),scale=0.3)
# torus = obj_reader.get_mesh('Torus', position=(0, 0, -3),scale=0.5)
# torus2 = obj_reader.get_mesh('Torus', position=(0, 0, -3),scale=0.5)


# #set up diffuse color for meshes
# sphere.uniforms['diffuse'] = [.6, .6, .6]
# torus.uniforms['diffuse'] = [1, 0, 0]
# torus2.uniforms['diffuse'] = [0, 0, 1]

# #add meshes to scene
# scene = rc.Scene(meshes=[sphere,torus,torus2])

# #set up scene background color
# scene.bgColor = 138/255, 113/255, 145/255

# #Default stats label to be displayed
# stats = ['Fall Status: False','Accelerometer Readings: Nan,Nan,Nan','Fall Distance: Nan']

# #exit game condition
# end_game=False

# # Constantly-Running mesh rotation, for fun
# def update(dt):
#     torus.rotation.y += 40. * dt
# pyglet.clock.schedule(update)


# # Constantly checks for new user inputs and processes it accordingly
# def user_inputs(dt):
#     if keys[key.R]:
#         #reset Everything 
#         torus.rotation.y = 0
#         torus2.rotation.x = 90
#         stats = ['Fall Status: False','Accelerometer Readings: Nan,Nan,Nan','Fall Distance: Nan']

#     if keys[key.ESCAPE]:
#         #quiting the display
#         exit_game= True
        
# pyglet.clock.schedule(user_inputs)


# @window.event
# def on_resize( width, height ):
#     ratio = 108/192
#     window.set_size( int(width), int(width*ratio) )


# # Draw Function
# @window.event
# def on_draw():
#     torus2.rotation.x = 90
    
#     if stats[0] =='Fall Status: False':
#         scene.bgColor = 138/255, 113/255, 145/255
#     else:
#         scene.bgColor = 12/255, 100/255, 12/255
    


#     with rc.default_shader:
#         scene.draw()

#     for i in range(len(stats)):
#         # printing out read in stats loop
#         label = pyglet.text.Label(stats[i],
#                           font_name='Times New Roman',
#                           font_size=12,
#                           x=10, y=window.height//2-window.height//3 -20*i,
#                           anchor_x='left', anchor_y='center')
#         label.draw()
#     if end_game == True:
#          pyglet.app.EventLoop().exit()




# # Pyglet's event loop run function
# pyglet.app.run()
