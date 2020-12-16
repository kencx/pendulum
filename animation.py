import numpy as np
from random import choice
import matplotlib.pyplot as plt
from matplotlib import animation, cm, rc
from methods import wrapping

# rc('text', usetex=True)
# rc('font', family='serif')

'''
add file name into save argument
find a way to incorporate time into animate functions, and allow it to control the time for the pendulum functions
'''

time = 30
N = 1000
timestep = time/(N-1)
T = np.linspace(0, time, N)

def animate_pendulum(system, hide_path=False, hide_axis=True, save=False):

    '''
    Generates an animation of a system of pendulums (without graphs)

    Args:
    system (list): system of pendulum(s) to be simulated
    hide_path (bool): hide trails of pendulum
    hide_axis (bool): default True hides axis of simulation
    save (bool): default True saves mp4 file of simulation
    '''

    state = system.state_array

    max_l = max([p.length for p in system.pendulums]) # max length among all pendulums

    fig = plt.figure(figsize=(6,6))
    ax = plt.axes(xlim=(-(max_l+1), max_l+1), ylim=(-(max_l+1), max_l+1)) # set axis limits
    ax.set_aspect('equal')

    if hide_axis:
        plt.axis('off')

    # text for running time
    time_temp = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    # initialize lines and paths
    lines, paths = [], []

    # colour map
    cmap = cm.get_cmap('rainbow')

    # for each pendulum, generate a line and path obj
    for i in range(len(state)):
        lobj = ax.plot([],[],'o-',lw=1.5, c=cmap(0.1*i))[0]
        lines.append(lobj)
        
        if not hide_path:
            pobj = ax.plot([],[],'--',lw=0.5, c=cmap(0.1*i), alpha = 0.7)[0]
            paths.append(pobj)

    # Initialize base frame
    # def init():
    #     for l in range(len(lines)):
    #         lines[l].set_data([],[]) # Sets line data to nothing
    #         paths[l].set_data([],[])
    #     time_text.set_text('')
    #     return lines, paths, time_text

    def animate(i):

        for lnum in range(len(lines)):
            
            if not system.double: # for single pendulums

                # position of pendulum
                x = [0, state[lnum][i,0]] # 0 is required to set pivot at the origin
                y = [0, state[lnum][i,1]]

                if not hide_path:
                    # path of pendulum
                    path_x = state[lnum][:i,0]
                    path_y = state[lnum][:i,1]
            
            else: 
                # for double pendulums
                x = [0, state[lnum][i,0], state[lnum][i,1]] # 0 is required to set pivot at the origin
                y = [0, state[lnum][i,2], state[lnum][i,3]]
            
                if not hide_path:
                    path_x = state[lnum][:i,1]
                    path_y = state[lnum][:i,3]

            lines[lnum].set_data(x,y)
            if not hide_path:
                paths[lnum].set_data(path_x, path_y)

        time_text.set_text(time_temp % (i*timestep))
        return lines, paths, time_text

    # Animation object
    anim = animation.FuncAnimation(fig, animate, frames=N, interval=30)

    if save:
        anim.save('_tests/animation.gif', writer='imagemagick', fps=30)

    plt.show()



def animate_pend_graph(system, graph, hide_axis=False, save=False):
    
    '''
    Animates a double pendulum system and with a graph of:
        displacement: Plots theta2 against theta1
        phase space: Plots angular velocity against angular displacement

    Args:
    system (list): system of pendulum(s) to be simulated
    graph (str): Takes strings of 'displacement' or 'phase space' and draws the specificed graph.
    # time (int): time to run simulation
    hide_axis (bool): default True hides axis of simulation
    save (bool): default True saves mp4 file of simulation
    '''

    state = system.state_array
    max_l = max([pendulum.length for pendulum in system.pendulums]) # max length among all pendulums

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,8))

    if graph == 'phase space':
        ax1.set_xlabel('theta (rad)')
        ax1.set_ylabel('omega (rad/s)')

    if graph == 'displacement': 
        ax1.set_xlabel('theta1 (rad)')
        ax1.set_ylabel('theta2 (rad)')

    ax2.set_xlim(-(max_l+1), max_l+1) # set axis limits
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

    # colour map
    cmap = cm.get_cmap('Spectral')

    # for each pendulum, generate graph, line and path objects
    for i in range(len(state)):
        gobj = ax1.plot([],[], '-', ms=1, c='r')[0]

        # pendulum objects
        lobj = ax2.plot([],[], 'o-', lw=1.5, c=cmap(0.1*i))[0]
        pobj = ax2.plot([],[], '--', lw=0.5, c=cmap(0.1*i), alpha = 0.7)[0]

        lines1.append(gobj)
        lines2.append(lobj)
        paths2.append(pobj)


    # list of arrays of theta1 and theta2 for all N
    graph_coords = []

    for p in system.pendulums:
        if graph == 'displacement':
            # graph_coords.append([p.states[0], p.states[1]]) 
            graph_coords.append(p.states[:,:2])

        if graph == 'phase space':
            p.states[:,0] = list(map(lambda x: wrapping(x), p.states[:,0])) # converts to -pi, pi range
            graph_coords.append(p.states[:,0:3:2])
            # pendulum.states[0] = list(map(lambda x: wrapping(x), pendulum.states[0])) 
            # graph_coords.append([pendulum.states[0], pendulum.states[2]])
        

    def animate(i):

        # for each pendulum in system
        for lnum in range(len(state)):

            if i == 0:
                graph_x, graph_y = [0], [0] # set initial axis limit

            else:
                graph_x = graph_coords[lnum][:i,0]
                graph_y = graph_coords[lnum][:i,1]

            x = [0, state[lnum][i,0], state[lnum][i,1]] # 0 is required to set pivot at the origin
            y = [0, state[lnum][i,2], state[lnum][i,3]]

            path_x = state[lnum][:i,1]
            path_y = state[lnum][:i,3]

            lines1[lnum].set_data(graph_x, graph_y)
            lines2[lnum].set_data(x, y)
            paths2[lnum].set_data(path_x, path_y)

            xmin, xmax = ax1.get_xlim()
            ymin, ymax = ax1.get_ylim()
            if (max(graph_x) > xmax) or (min(graph_x) < xmin) or (max(graph_y) > ymax) or (min(graph_y) < ymin):
                ax1.set_xlim(min(graph_x), max(graph_x)) # dynamic axis limits
                ax1.set_ylim(min(graph_y), max(graph_y))

        time_text.set_text(time_temp % (i*timestep))
        return lines1, lines2, paths2, time_text


    # Animation object
    anim = animation.FuncAnimation(fig, animate, frames=N, interval=30)

    if save:
        anim.save('_tests/single_animation.gif', writer='imagemagick', fps=30)

    plt.show()