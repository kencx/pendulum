import numpy as np
from scipy.integrate import odeint
from methods import Derivatives, rk4, euler


class Pendulum():

    g = 9.81
    t = 30
    N = 1000
    timestep = t/(N-1)
    T = np.linspace(0, t, N)

    '''
    Args:

    Length (float): length of massless string from pivot to weight
    Mass (float): mass of weight suspended
    Theta (float): initial angle of displacement
    Omega (float): initial angular velocity

    State (array): Array of anglular displacement and angular velocity
    Solution (array): Array of states of pendulum at each dt
    Position (array): Array of x and y coordinates of pendulum at each dt
    '''

    def __init__(self, length, mass, theta, omega, method=odeint):
        self.length = length
        self.mass = mass
        self.theta = np.radians(theta)
        self.omega = omega
        self.state = np.array([np.radians(theta), omega])
        self.solution = self.sol(method)
        self.position = self.get_pos()


    def get_pos(self):
        '''
        input: solution state of pendulum at timestep dt
        output: x, y coordinates of pendulum at timestep dt
        '''
        x_coord = self.length*np.sin(self.solution[:,0])
        y_coord = -self.length*np.cos(self.solution[:,0])
        return [x_coord,y_coord]


    def sol(self, method):

        '''
        output: solution state of pendulum
        '''

        if method == rk4 or method == euler:
            f = np.zeros([self.N,2])

            f[0,0], f[0,1] = self.state[0], self.state[1]

            for j in range(self.N-1):
                f[j+1] = method(f[j], 0, self.timestep, Derivatives.pend, self.length, self.g)
            
            return f

        if method == odeint:
            return odeint(Derivatives.pend, self.state, self.T, (self.length, self.g))



class Double_Pendulum:

    g = 9.81
    t = 30
    N = 1000
    timestep = t/(N-1)
    T = np.linspace(0, t, N)


    def __init__(self, p1, p2, method=odeint):

        '''
        Variables:

        p1: Pendulum 1 (attached to pivot)
        p2: Pendulum 2 (attached to Pendulum 1)
        '''

        self.p1 = p1
        self.p2 = p2
        self.length = p1.length + p2.length
        self.state = np.array([p1.theta, p2.theta, p1.omega, p2.omega])
        self.solution = self.sol(method)
        self.position = self.get_pos()


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


    def sol(self, method):

        if method == rk4 or method == euler:
            f = np.zeros([self.N, 4])

            f[0,0], f[0,1], f[0,2], f[0,3] = self.state[0], self.state[1], self.state[2], self.state[3]

            for j in range(self.N-1):
                f[j+1] = method(f[j], 0, self.timestep, Derivatives.double_pend, self.p1.length, self.p2.length, self.p1.mass, self.p2.mass, self.g)
            
            return f

        if method == odeint:
            return odeint(Derivatives.double_pend, self.state, self.T, (self.p1.length, self.p2.length, self.p1.mass, self.p2.mass, self.g))
