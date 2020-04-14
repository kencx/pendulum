import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from pendulum import Pendulum, Double_Pendulum
from animation import animate_pendulum


class system:

    '''
    Args:

    pendulums (list): list of pendulums

    double_present (bool): Check if double pendulums are present among input pendulums
    state (array): Array of pendulum states at dt

    '''
    def __init__(self, pendulums):
        self.pendulums = pendulums
        self.double_present = self.double_present() # check if any double pendulums present
        self.state = self.state()

    def state(self):
        final_state = []

        if self.double_present:
            for pendulum in self.pendulums:
                final_state.append((pendulum.position[0], pendulum.position[1], pendulum.position[2], pendulum.position[3])) # (x1, x2, y1, y2)
        else:
            for pendulum in self.pendulums:
                final_state.append((pendulum.position[0], pendulum.position[1])) # (x, y)

        return final_state

    def double_present(self):
        return any(isinstance(pendulum,Double_Pendulum) for pendulum in self.pendulums)



def test_example():
    pendulum1 = Pendulum(1.0, 2.0, 150, 0)
    pendulum2 = Pendulum(1.0, 2.0, 150, 0)
    pendulum3 = Double_Pendulum(pendulum1, pendulum2)
    test_system = system(pendulums)
    animate_pendulum(test_system, 30)

test_example()
