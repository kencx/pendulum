import numpy as np
from pendulum import Pendulum, Double_Pendulum

class system:

    '''
    Args:

    pendulums (list): list of pendulums

    double (bool): Check if double pendulums are present among input pendulums
    state (array): Array of pendulum states at dt

    '''
    def __init__(self, pendulums):
        self.pendulums = pendulums
        self.double = self.double() # check if any double pendulums present
        self.state = self.state()

    def state(self):
        final_state = []

        if self.double:
            for pendulum in self.pendulums:
                final_state.append((pendulum.position[0], pendulum.position[1], pendulum.position[2], pendulum.position[3])) # (x1, x2, y1, y2)
        else:
            for pendulum in self.pendulums:
                final_state.append((pendulum.position[0], pendulum.position[1])) # (x, y)

        return final_state

    def double(self):
        return any(isinstance(pendulum,Double_Pendulum) for pendulum in self.pendulums)


    def energy_check(self):
        pass

