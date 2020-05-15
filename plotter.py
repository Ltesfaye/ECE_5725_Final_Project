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

        #display label
        self.label = plt.gcf().text(0.02, 0.5, labels, fontsize=9)

        #plot labels
        self.pitch_figure.set_title('Pitch over time')
        self.roll_figure.set_title("Roll over time")
        self.map.suptitle('Visualizing phone fall')
      

        #Axis values for the plotter
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
        left  = 0.125  # the left side of the subplots of the figure
        right = 0.9    # the right side of the subplots of the figure
        bottom = 0.1   # the bottom of the subplots of the figure
        top = 0.9      # the top of the subplots of the figure
        wspace = 0.2   # the amount of width reserved for blank space between subplots
        hspace = 1  # the amount of height reserved for white space between subplots
        
        plt.subplots_adjust(left=left, bottom=bottom, right=right, top=top, wspace=wspace, hspace=hspace)

       
    
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

    def update_label(self,new_label,initial=False):
        self.label.set_visible(False)
        self.label=  plt.gcf().text(0.02, 0.5, new_label, fontsize=9)
        self.draw()


    def add_pitch_value(self,p,block=False):
        self.hl_pitch.set_xdata(np.append(self.hl_pitch.get_xdata(), self.pitch_counter))
        self.hl_pitch.set_ydata(np.append(self.hl_pitch.get_ydata(), p))
        self.pitch_counter +=1
        self.pitch_figure.set_xlim([0,self.pitch_counter])
        plt.draw()
        self.draw()
    
    def add_roll_value(self, p,block=False):
        self.hl_roll.set_xdata(np.append(self.hl_roll.get_xdata(), self.roll_counter))
        self.hl_roll.set_ydata(np.append(self.hl_roll.get_ydata(), p))
        self.roll_counter +=1
        self.roll_figure.set_xlim([0,self.roll_counter])
        plt.draw()
        self.draw()

        
    def add_3d_point(self, p, block= False , pause=True):
        self.update_3d_line(self.hl, p)
        self.draw()
        if block:
            plt.show(block=block)
        if pause:
            plt.pause(0.001)
    
    def start(self):
        fig = plt.gcf()
        fig.show()
        fig.canvas.draw()

    def draw(self):
        plt.gcf().canvas.draw()

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



      
