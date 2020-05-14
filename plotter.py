# from matplotlib import pyplot as plt
# import numpy as np
# import mpl_toolkits.mplot3d.axes3d as p3
# from matplotlib import animation

# fig = plt.figure()
# ax = p3.Axes3D(fig)

# def gen(n):
#     phi = 0
#     while phi < 2*np.pi:
#         yield np.array([np.cos(phi), np.sin(phi), phi])
#         phi += 2*np.pi/n

# def update(num, data, line):
#     line.set_data(data[:2, :num])
#     line.set_3d_properties(data[2, :num])

# N = 100
# data = np.array(list(gen(N))).T
# line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

# # Setting the axes properties
# ax.set_xlim3d([-1.0, 1.0])
# ax.set_xlabel('X')

# ax.set_ylim3d([-1.0, 1.0])
# ax.set_ylabel('Y')

# ax.set_zlim3d([0.0, 10.0])
# ax.set_zlabel('Z')

# ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=10000/N, blit=False)
# #ani.save('matplot003.gif', writer='imagemagick')
# plt.show()

import numpy as np 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
 
 
 
def update_line(hl, new_data):
	xdata, ydata, zdata = hl._verts3d
	hl.set_xdata(list(np.append(xdata, new_data[0])))
	hl.set_ydata(list(np.append(ydata, new_data[1])))
	hl.set_3d_properties(list(np.append(zdata, new_data[2])))
	plt.draw()
 
 
map = plt.figure()
map_ax = Axes3D(map)
# map_ax.autoscale(enable=True, axis='both', tight=True)
# map_ax.auto_scale_xyz()

 
# # # Setting the axes properties
# map_ax.set_xlim3d([0.0, 10.0])
# map_ax.set_ylim3d([0.0, 10.0])
# map_ax.set_zlim3d([0.0, 10.0])
 
hl, = map_ax.plot3D([0], [0], [0])
 
update_line(hl, (2,2, 1))
map_ax.relim()
map_ax.autoscale_view()
plt.show(block=False)
plt.pause(1)
 
update_line(hl, (5,5, 5))
map_ax.relim()
map_ax.autoscale_view()
plt.show(block=False)
plt.pause(2)
 
update_line(hl, (-8,-1,- 4))
map_ax.relim()
map_ax.autoscale_view()
plt.show(block=True)