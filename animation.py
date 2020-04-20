import numpy as np
from random import choice
import matplotlib.pyplot as plt
from matplotlib import animation


def animate_pendulum(system, time, hide_axis=True, save=False):

    '''
    Args:
    system (list): system of pendulum(s) to be simulated
    time (int): time to run simulation
    hide_axis (bool): default True hides axis of simulation
    save (bool): default True saves mp4 file of simulation

    '''

    N = 1000
    timestep = time/(N-1)
    T = np.linspace(0, time, N)

    state = system.state
    max_l = max([pendulum.length for pendulum in system.pendulums]) # max length among all pendulums

    fig = plt.figure()
    ax = plt.axes(xlim=(-(max_l+1), max_l+1), ylim=(-(max_l+1), max_l+1))
    ax.set_aspect('equal')

    if hide_axis:
        plt.axis('off')
    
    # text for running time
    time_temp = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    # initialize lines and paths
    lines = []
    paths = []

    colours = ['b', 'g', 'k', 'o', 'c', 'm']

    # for each pendulum
    for i in range(len(state)):
        lobj = ax.plot([],[],'o-',lw=1.5, c=choice(colours))[0]
        pobj = ax.plot([],[],'--',lw=0.5, c=choice(colours), alpha = 0.7)[0]
        lines.append(lobj)
        paths.append(pobj)

    # Initialize base frame
    # def init():
    #     for l in range(len(lines)):
    #         lines[l].set_data([],[]) # Sets line data to nothing
    #         paths[l].set_data([],[])
    #     time_text.set_text('')
    #     return lines, paths, time_text

    def single_pend_animate(i):

        for lnum in range(len(lines)):
            x = [0, state[lnum][0][i]]
            y = [0, state[lnum][1][i]]

            path_x = [state[lnum][0][i] for i in range(0,i)]
            path_y = [state[lnum][1][i] for i in range(0,i)]

            lines[lnum].set_data(x,y)
            paths[lnum].set_data(path_x, path_y)

        time_text.set_text(time_temp % (i*timestep))
        return lines, paths, time_text


    def double_pend_animate(i):

        for lnum in range(len(lines)):
            x = [0, state[lnum][0][i], state[lnum][1][i]]
            y = [0, state[lnum][2][i], state[lnum][3][i]]

            path_x = [state[lnum][1][i] for i in range(0,i)]
            path_y = [state[lnum][3][i] for i in range(0,i)]

            lines[lnum].set_data(x, y)
            paths[lnum].set_data(path_x, path_y)

        time_text.set_text(time_temp % (i*timestep))
        return lines, paths, time_text


    # Animation object
    if system.double:
        anim = animation.FuncAnimation(
                                fig,
                                double_pend_animate,    # animate(frames)
                                # init_func=init,
                                frames=np.arange(1, len(T)),
                                interval=30,
                                blit=False
                                )
    else:
        anim = animation.FuncAnimation(
                                fig,
                                single_pend_animate,    # animate(frames)
                                # init_func=init,
                                frames=np.arange(1, len(T)),
                                interval=30,
                                blit=False
                                )

    plt.show()


    # if save:
    #     anim.save('pendulum.mp4')

