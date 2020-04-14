import numpy as np
from scipy.integrate import odeint

t = 30
N = 1000
timestep = t/(N-1)
T = np.linspace(0,t,N)

class Pendulum:

    '''
    Args:

    Length (int): length of massless string from pivot to weight
    Mass (int): mass of weight suspended
    Theta (int): initial angle of displacement
    Omega (int): initial angular velocity

    State (array): Array of anglular displacement and angular velocity
    Solution (array): Array of states of pendulum at each dt
    Position (array): Array of x and y coordinates of pendulum at each dt
    '''

    def __init__(self, length, mass, theta, omega):
        self.length = length
        self.mass = mass
        self.g = 9.81
        self.theta = np.radians(theta)
        self.omega = omega
        self.state = np.array([np.radians(theta), omega])
        self.solution = self.sol()
        self.position = self.get_pos()

    def pend(state, time, length, g):
        '''
        input: state of pendulum
        output: derivative of input state
        '''
        x_dot = state[1]
        v_dot = -(g/length)*np.sin(state[0])
        return np.array([x_dot, v_dot])

    def get_pos(self):
        '''
        input: solution state of pendulum at timestep dt
        output: x, y coordinates of pendulum at timestep dt
        '''
        x_coord = self.length*np.sin(self.solution[:,0])
        y_coord = -self.length*np.cos(self.solution[:,0])
        return [x_coord,y_coord]

    def sol(self):
        '''
        output: solution state of pendulum
        '''
        return odeint(Pendulum.pend, self.state, T, (self.length, self.g))


class Double_Pendulum:
    def __init__(self, p1, p2):

        '''
        Variables:

        p1: Pendulum 1 (attached to pivot)
        p2: Pendulum 2 (attached to Pendulum 1)
        '''

        self.p1 = p1
        self.p2 = p2
        self.state = np.array([p1.theta, p2.theta, p1.omega, p2.omega])
        self.solution = self.sol()
        self.position = self.get_pos()

    def double_pend(state, time, l1, l2, m1, m2, g):
        '''
        input: state of pendulum
        output: derivative of input state
        '''
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

    def get_pos(self):
        '''
        input: solution state of pendulum at timestep dt
        output: x, y coordinates of pendulum at timestep dt
        '''
        x1 = self.p1.length*np.sin(self.solution[:,0])
        x2 = x1+ self.p2.length*np.sin(self.solution[:,1])
        y1 = -self.p1.length*np.cos(self.solution[:,0])
        y2 = y1 - self.p2.length*np.cos(self.solution[:,1])
        return [x1, x2, y1, y2]

    def sol(self):
        return odeint(Double_Pendulum.double_pend, self.state, T, (self.p1.length, self.p2.length, self.p1.mass, self.p2.mass, self.p1.g))
