import numpy as np
from methods import Derivative, rk4

g = 9.81
t = 30
N = 1000
timestep = t/(N-1)
T = np.linspace(0, t, N)

class Pendulum():

    '''
    Args:

    Length (float): length of massless string from pivot to weight
    Mass (float): mass of weight suspended
    Theta (float): initial angle of displacement (in deg)
    Omega (float): initial angular velocity

    State (array): Array of anglular displacement and angular velocity
    Solution (array): Array of states of system at each timestep
    Position (array): Array of x and y coordinates of system at each timestep
    '''

    def __init__(self, length, mass, theta, omega):
        self.length = length
        self.mass = mass
        self.theta = np.radians(theta)
        self.omega = omega

        self.states = np.zeros([N,2])
        self.initial_state = self.initial_state() # set initial state
        self.solution = self.get_solution() 
        self.position = self.get_position()


    def initial_state(self):
        self.states[0,:] = [self.theta, self.omega]

    def get_solution(self):

        for j in range(N-1):
            self.states[j+1,:] = rk4(self.states[j,:], 0, timestep, Derivative.pend, self.length, g)
        
        return self.states

    def get_position(self):
        positions = np.zeros(self.states.shape)
        positions[:,0] = self.length*np.sin(self.solution[:,0])
        positions[:,1] = -self.length*np.cos(self.solution[:,0])
        return positions


class Double_Pendulum:

    def __init__(self, p1, p2):

        '''
        Args:

        p1 (Pendulum class): Pendulum 1 (attached to pivot)
        p2 (Pendulum class): Pendulum 2 (attached to Pendulum 1)

        states (array): Array of state variables 
        '''

        self.p1 = p1
        self.p2 = p2
        self.length = p1.length + p2.length # total length

        self.states = np.zeros([N,4])
        self.initial_state = self.initial_state() # set initial state
        self.solution = self.get_solution()
        self.position = self.get_position()

        
    def initial_state(self):
        self.states[0,:] = [self.p1.theta, self.p2.theta, self.p1.omega, self.p2.omega]

    def get_solution(self):

        for j in range(N-1):
            self.states[j+1,:] = rk4(self.states[j,:], 0, timestep, Derivative.double_pend, self.p1.length, self.p2.length, self.p1.mass, self.p2.mass, g)
        
        return self.states

    def get_position(self):
        positions = np.zeros(self.states.shape)
        x1 = self.p1.length*np.sin(self.solution[:,0])
        positions[:,0] = x1
        positions[:,1] = x1 + self.p2.length*np.sin(self.solution[:,1])
        y1 = -self.p1.length*np.cos(self.solution[:,0])
        positions[:,2] = y1
        positions[:,3] = y1 - self.p2.length*np.cos(self.solution[:,1])
        return positions


