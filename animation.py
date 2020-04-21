import numpy as np
from random import choice
import matplotlib.pyplot as plt
from matplotlib import animation, cm, rc

# rc('text', usetex=True)
# rc('font', family='serif')

time = 30
N = 1000
timestep = time/(N-1)
T = np.linspace(0, time, N)

def animate_pendulum(system, hide_axis=True, save=False):

    '''
    Args:
    system (list): system of pendulum(s) to be simulated
    # time (int): time to run simulation
    hide_axis (bool): default True hides axis of simulation
    save (bool): default True saves mp4 file of simulation

    '''

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
    lines, paths = [], []

    cmap = cm.get_cmap('Spectral')

    # for each pendulum
    for i in range(len(state)):
        lobj = ax.plot([],[],'o-',lw=1.5, c=cmap(0.1*i))[0]
        pobj = ax.plot([],[],'--',lw=0.5, c=cmap(0.1*i), alpha = 0.7)[0]
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

    if save:
        anim.save('_tests/animation.gif', writer='imagemagick', fps=30)

    plt.show()



def animate_pend_with_graph(system, hide_axis=False, save=False):

    '''
    Animates a double pendulum system and draws a graph of theta2 against theta1

    '''

    state = system.state
    max_l = max([pendulum.length for pendulum in system.pendulums]) # max length among all pendulums

    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.set_xlabel('theta1 (rad)')
    ax1.set_ylabel('theta2 (rad)')

    ax2.set_xlim(-(max_l+1), max_l+1)
    ax2.set_ylim(-(max_l+1), max_l+1)
    ax2.set_aspect('equal')

    if hide_axis:
        # ax1.axis('off')
        ax2.axis('off')

    # text for running time
    time_temp = 'time = %.1fs'
    time_text = ax2.text(0.05, 0.9, '', transform=ax2.transAxes)


    # initialize lines and paths
    lines1 = []
    lines2, paths2 = [], []

    cmap = cm.get_cmap('Spectral')

    # for each pendulum
    for i in range(len(state)):
        gobj = ax1.plot([],[], '-', lw=1, c='r')[0]
        lobj = ax2.plot([],[], 'o-', lw=1.5, c=cmap(0.1*i))[0]
        pobj = ax2.plot([],[], '--', lw=0.5, c=cmap(0.1*i), alpha = 0.7)[0]
        lines1.append(gobj)
        lines2.append(lobj)
        paths2.append(pobj)


    # def single_pend_animate(i):

    #     for lnum in range(len(lines)):
    #         x = [0, state[lnum][0][i]]
    #         y = [0, state[lnum][1][i]]

    #         path_x = [state[lnum][0][i] for i in range(0,i)]
    #         path_y = [state[lnum][1][i] for i in range(0,i)]

    #         lines[lnum].set_data(x,y)
    #         paths[lnum].set_data(path_x, path_y)

    #     time_text.set_text(time_temp % (i*timestep))
    #     return lines, paths, time_text


    # list of tuples of arrays of theta1 and theta2 for all N
    graph_coords = []
    for pendulum in system.pendulums:
        graph_coords.append([pendulum.states[0], pendulum.states[1]])

    def double_pend_animate(i):

        # for each pendulum
        for lnum in range(len(state)):

            graph_x = [graph_coords[lnum][0][i] for i in range(0,i)]
            graph_y = [graph_coords[lnum][1][i] for i in range(0,i)]

            x = [0, state[lnum][0][i], state[lnum][1][i]]
            y = [0, state[lnum][2][i], state[lnum][3][i]]

            path_x = [state[lnum][1][i] for i in range(0,i)]
            path_y = [state[lnum][3][i] for i in range(0,i)]

            lines1[lnum].set_data(graph_x, graph_y)
            lines2[lnum].set_data(x, y)
            paths2[lnum].set_data(path_x, path_y)

            xmin, xmax = ax1.get_xlim()
            ymin, ymax = ax1.get_ylim()
            if (max(graph_x) >= xmax) or (min(graph_x) <= xmin) or (max(graph_y) >= ymax) or (min(graph_y) <= ymin):
                ax1.set_xlim(min(graph_x), max(graph_x))
                ax1.set_ylim(min(graph_y), max(graph_y))

        time_text.set_text(time_temp % (i*timestep))
        return lines1, lines2, paths2, time_text


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
    # else:
    #     anim = animation.FuncAnimation(
    #                             fig,
    #                             single_pend_animate,    # animate(frames)
    #                             # init_func=init,
    #                             frames=np.arange(1, len(T)),
    #                             interval=30,
    #                             blit=False
    #                             )

    if save:
        anim.save('_tests/animation.gif', writer='imagemagick', fps=30)

    plt.show()
