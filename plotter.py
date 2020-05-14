import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
 
class Plotter:
    def __init__(self,labels):
          
        self.map = plt.figure(figsize=plt.figaspect(2.))

        self.map.canvas.manager.full_screen_toggle() # toggle fullscreen mode
        
        #figures for drawing the position,pitch and roll
        self.map_ax = self.map.add_subplot(1, 2, 1, projection='3d')
        self.pitch_figure = self.map.add_subplot(2, 2, 2)
        self.roll_figure = self.map.add_subplot(2, 2, 4)

        self.label = plt.gcf().text(0.02, 0.5, labels, fontsize=14)

        #plot labels
        self.pitch_figure.set_title('Pitch over time')
        self.roll_figure.set_title("Roll over time")
        self.map.suptitle('Visualizing phone fall')
      
  

        self.hl, = self.map_ax.plot3D([0], [0], [0])
        self.hl_pitch, = self.pitch_figure.plot([],[])
        self.hl_roll,  = self.roll_figure.plot([],[])

        # # # Setting the axes scale properties
        self.pitch_counter=  0
        self.roll_counter= 0

        self.x_range = [0.0,10.0]
        self.y_range = [0.0,10.0]
        self.z_range = [0.0,10.0]
        
        self.map_ax.set_xlim3d(self.x_range)
        self.map_ax.set_ylim3d(self.y_range)
        self.map_ax.set_zlim3d(self.z_range)
        
        self.roll_figure.set_ylim([-360,360])
        self.pitch_figure.set_ylim([-360,360])

       
        
    
    def update_3d_ranges(self,new_data):
        self.x_range = [min(self.x_range[0],new_data[0]), max(self.x_range[1],new_data[0])]
        self.y_range = [min(self.y_range[0],new_data[1]), max(self.y_range[1],new_data[1])]
        self.z_range = [min(self.z_range[0],new_data[2]), max(self.z_range[1],new_data[2])]
        
        self.map_ax.set_xlim3d(self.x_range)
        self.map_ax.set_ylim3d(self.y_range)
        self.map_ax.set_zlim3d(self.z_range)

      
    def update_3d_line(self,hl, new_data):
        xdata, ydata, zdata = hl._verts3d
        hl.set_xdata(list(np.append(xdata, new_data[0])))
        hl.set_ydata(list(np.append(ydata, new_data[1])))
        hl.set_3d_properties(list(np.append(zdata, new_data[2])))
        self.update_3d_ranges(new_data)
        plt.draw()
    
    def reset_pitch(self):
        self.hl_pitch.set_xdata([])
        self.hl_pitch.set_ydata([])
        self.pitch_counter = 0
    def reset_roll(self):
        self.hl_roll.set_xdata([])
        self.hl_roll.set_ydata([])
        self.roll_counter=0
    
    def reset_pitch_roll(self):
        self.reset_pitch()
        self.reset_roll()

    def update_label(self,new_label):
        self.label.set_visible(False)
        self.label=  plt.gcf().text(0.02, 0.5, new_label, fontsize=9)
        plt.draw()
        plt.show(block=False)

    def add_pitch_value(self,p,block=False):
        self.hl_pitch.set_xdata(np.append(self.hl_pitch.get_xdata(), self.pitch_counter))
        self.hl_pitch.set_ydata(np.append(self.hl_pitch.get_ydata(), p))
        self.pitch_counter +=1
        self.pitch_figure.set_xlim([0,self.pitch_counter])
        plt.draw()
        plt.show(block=block)
    
    def add_roll_value(self, p,block=False):
        self.hl_roll.set_xdata(np.append(self.hl_roll.get_xdata(), self.roll_counter))
        self.hl_roll.set_ydata(np.append(self.hl_roll.get_ydata(), p))
        self.roll_counter +=1
        self.roll_figure.set_xlim([0,self.roll_counter])
        plt.draw()
        plt.show(block=block)
        
    def add_3d_point(self, p, block= False , pause=True):
        self.update_3d_line(self.hl, p)
        plt.show(block=block)
        if pause:
            plt.pause(0.5)
    
    def start(self):
        self.add_3d_point((0,0,0))

    def run_test(self):
        
        self.add_pitch_value(10)
        self.add_roll_value(10)
        self.add_3d_point((2,2, 1))
        self.add_roll_value(20)
        self.add_pitch_value(20)

        
        self.add_3d_point((5,5, 5))
        self.update_label("WHAT>>>>")
        self.add_3d_point((-5,35,- 5))

     

        
        self.add_3d_point((8,8, 8),block=True)


# plot = Plotter('HI')
# plot.run()
      
 
 



 


 

 



# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

# import matplotlib.pyplot as plt
# import numpy as np


# def f(t):
#     return np.cos(2*np.pi*t) * np.exp(-t)


# # Set up a figure twice as tall as it is wide
# fig = plt.figure(figsize=plt.figaspect(2.))
# fig.suptitle('A tale of 2 subplots')

# # First subplot
# ax = fig.add_subplot(2, 1, 1)

# t1 = np.arange(0.0, 5.0, 0.1)
# t2 = np.arange(0.0, 5.0, 0.02)
# t3 = np.arange(0.0, 2.0, 0.01)

# ax.plot(t1, f(t1), 'bo',
#         t2, f(t2), 'k--', markerfacecolor='green')
# ax.grid(True)
# ax.set_ylabel('Damped oscillation')

# # Second subplot
# ax = fig.add_subplot(2, 1, 2, projection='3d')

# X = np.arange(-5, 5, 0.25)
# Y = np.arange(-5, 5, 0.25)
# X, Y = np.meshgrid(X, Y)
# R = np.sqrt(X**2 + Y**2)
# Z = np.sin(R)

# surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
#                        linewidth=0, antialiased=False)
# ax.set_zlim(-1, 1)

# plt.show()