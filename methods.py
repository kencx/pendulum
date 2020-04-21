import numpy as np

def euler(f, t, dt, derivs, *args):

    '''
    Euler method

    Args:
    f (array): y_i
    derivs (func): derivates
    t (int): time

    Outputs: y_(i+1)
    '''

    if derivs == Derivatives.pend:
        return f + derivs(f, t, args[0], args[1]) * dt
    
    elif derivs == Derivatives.double_pend:
        return f + derivs(f, t, args[0], args[1], args[2], args[3], args[4]) * dt


def rk4(f, t, dt, derivs, *args):

    '''
    Runge-Kutta 4 method

    Args:
    f (array): y_i
    derivs (func): derivates
    t (int): time

    Outputs: y_(i+1)
    '''
    
    if derivs == Derivatives.pend:
        k1 = derivs(f, t, args[0], args[1]) * dt
        k2 = derivs(f + 0.5*k1, t + 0.5*dt, args[0], args[1]) * dt
        k3 = derivs(f + 0.5*k2, t + 0.5*dt, args[0], args[1]) * dt
        k4 = derivs(f + k3, t + dt, args[0], args[1]) * dt
        return f + (k1 + 2*k2 + 2*k3 + k4)/6

    if derivs == Derivatives.double_pend:
        k1 = derivs(f, t, args[0], args[1], args[2], args[3], args[4]) * dt
        k2 = derivs(f + 0.5*k1, t + 0.5*dt, args[0], args[1], args[2], args[3], args[4]) * dt
        k3 = derivs(f + 0.5*k2, t + 0.5*dt, args[0], args[1], args[2], args[3], args[4]) * dt
        k4 = derivs(f + k3, t + dt, args[0], args[1], args[2], args[3], args[4]) * dt
        return f + (k1 + 2*k2 + 2*k3 + k4)/6



class Derivatives():

    @staticmethod
    def pend(state, t, l, g):

        '''
        input: state of simple pendulum
        output: derivative of input state
        '''

        x_dot = state[1] # dx/dt = v
        v_dot = -(g/l)*np.sin(state[0]) #dv/dt = -g/l * sin(x)
        return np.array([x_dot, v_dot])



    @staticmethod
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


    @staticmethod
    def spring_pend(state, time):
        pass