import numpy as np
from pendulum import Pendulum, Double_Pendulum

class system:

    '''
    Generates system of pendulums

    Args:

    pendulums (list): list of pendulums

    double (bool): Check if double pendulums are present in input list
    state (array): States of EACH pendulum

    '''
    def __init__(self, pendulums):
        self.pendulums = pendulums
        self.double = self.double() # check if any double pendulums are present
        self.state_array = self.state() 

    def state(self):
        state_array = []
        for p in self.pendulums:
            state_array.append(p.position) # (x1, x2, y1, y2)

        return state_array

    def double(self):
        return any(isinstance(pendulum,Double_Pendulum) for pendulum in self.pendulums)
