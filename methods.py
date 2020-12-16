import numpy as np
from math import pi


class Derivative():

    @staticmethod
    def pend(state, t, l, g):

        '''
        Derivative of the state of a simple pendulum

        Args: 
        state (array): State function
        t (int): Time
        l (float): Length of string
        g (float): Gravitational acceleration


        Output: Derivative of input state (array)
        '''

        x_dot = state[1] # dx/dt = v
        v_dot = -(g/l)*np.sin(state[0]) #dv/dt = -g/l * sin(x)
        return np.array([x_dot, v_dot])



    @staticmethod
    def double_pend(state, t, l1, l2, m1, m2, g):

        '''
        Derivate of the state of a double pendulum

        Args:
        state (array): State function
        t (int): Time
        l1, l2 (float): Length of string 1 and string 2
        m1, m2 (float): Mass of mass 1 and mass 2
        g (float): Gravitational acceleration

        Output: Derivative of input state
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


def rk4(f, t, dt, derivs, *args):

    '''
    Runge-Kutta 4 method

    Args:
    f (array): State function at time i
    t (int): Time
    dt (float): Timestep
    derivs (func): Derivate function
    args (float): Additional arguments required for derivs function


    Outputs: State function at time i+1
    '''

    # find a better way to run the function when different derivs function is passed
    
    if derivs == Derivative.pend:
        k1 = derivs(f, t, args[0], args[1]) * dt
        k2 = derivs(f + 0.5*k1, t + 0.5*dt, args[0], args[1]) * dt
        k3 = derivs(f + 0.5*k2, t + 0.5*dt, args[0], args[1]) * dt
        k4 = derivs(f + k3, t + dt, args[0], args[1]) * dt
        return f + (k1 + 2*k2 + 2*k3 + k4)/6

    if derivs == Derivative.double_pend:
        k1 = derivs(f, t, args[0], args[1], args[2], args[3], args[4]) * dt
        k2 = derivs(f + 0.5*k1, t + 0.5*dt, args[0], args[1], args[2], args[3], args[4]) * dt
        k3 = derivs(f + 0.5*k2, t + 0.5*dt, args[0], args[1], args[2], args[3], args[4]) * dt
        k4 = derivs(f + k3, t + dt, args[0], args[1], args[2], args[3], args[4]) * dt
        return f + (k1 + 2*k2 + 2*k3 + k4)/6



def wrapping(point):
    '''
    Restricts angles to -pi < x < pi

    Args:
    point (float): Point

    Output: Point within -pi < x < pi
    '''
    # change this to remove if, elif as it is unnecessary
    if point > pi:
        while point > pi:
            point -= 2*pi

    elif point < -pi:
        while point < -pi:
            point += 2*pi

    return point