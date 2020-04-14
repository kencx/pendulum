import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from scipy.integrate import odeint


# constants
m1 = 2.0
m2 = 2.0
l1 = 1.0
l2 = 1.0
g = 9.80665

t = 30
N = 1000
timestep = t/(N-1)
T = np.linspace(0,t,N)

# starting conditions
theta1 = np.radians(120) # initial angle
theta2 = np.radians(120)
omega1 = 0 # initial angular velocity
omega2 = 0

# Set initial state (angle, angular velocity)
states = np.array([theta1, theta2, omega1, omega2])

def double_pendulum(state,time):
    delta = state[1]-state[0]
    g0 = state[2]
    g1 = state[3]
    g2 = (m2*l1*state[2]*state[2]*np.sin(delta)*np.cos(delta) \
    + m2*g*np.sin(state[1])*np.cos(delta) + m2*l2*state[3]*state[3]*np.sin(delta) \
    - (m1+m2)*g*np.sin(state[0])) / ((m1+m2)*l1 - m2*l1*np.cos(delta)*np.cos(delta))
    g3 = ((-m2*l2*state[3]*state[3]*np.sin(delta)*np.cos(delta)) \
    + (m1+m2) * (g*np.sin(state[0])*np.cos(delta) - l1*state[2]*state[2]*np.sin(delta) - g*np.sin(state[1]))) \
    / ((m1+m2)*l2 - m2*l2*np.cos(delta)*np.cos(delta))
    return np.array([g0, g1, g2, g3])

def get_pos(state):
    x1 = l1*np.sin(state[:,0])
    x2 = x1+ l2*np.sin(state[:,1])
    y1 = -l1*np.cos(state[:,0])
    y2 = y1 - l2*np.cos(state[:,1])
    return (x1, x2, y1, y2)

# solving with integrate ODE
sol = odeint(double_pendulum,states,T)
x1_coord, x2_coord, y1_coord, y2_coord = get_pos(sol)

# path line
path_x = []
path_y = []

# Animation
fig = plt.figure()
ax = plt.axes(xlim=(-(l1+l2+0.5),l1+l2+0.5),ylim=(-(l1+l2+0.5),l1+l2+0.5))
plt.axis('off')
ax.set_aspect('equal')

line, = ax.plot([],[],'o-',lw=2) # Define the line object
path, = ax.plot([],[],'k.',lw=1) # Define path object
time_temp = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

# Initialize base frame
def init():
    line.set_data([],[]) # Sets line data to nothing
    path.set_data([],[])
    time_text.set_text('')
    return line, path, time_text

# Animation function
def animate(i):
    global path_x, path_y, path
    x = [0, x1_coord[i], x2_coord[i]]
    y = [0, y1_coord[i], y2_coord[i]]
    path_x += [x2_coord[i]]
    path_y += [y2_coord[i]]
    line.set_data(x, y)
    path.set_data(path_x, path_y)
    time_text.set_text(time_temp % (i*timestep))
    return line, path, time_text

# Animation object
anim = animation.FuncAnimation(fig, animate, init_func=init, frames=np.arange(1,len(T)), interval=20, blit=True) # animate(frames)
plt.show()
