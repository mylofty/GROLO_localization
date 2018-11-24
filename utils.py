# -*- coding:utf-8 -*-
#from tensor_position import *
import numpy as np
from matplotlib import pyplot as plt
from sympy import *
from scipy.optimize import fsolve
from mpl_toolkits.mplot3d import Axes3D
from Robot import *
import matplotlib.animation as animation
import copy
import math
from matplotlib import cm

times = 1

def distance(p1, p2):
    return np.sqrt(np.square(p1[0] - p2[0]) + np.square(p1[1] - p2[1]))


def show(points, robots):
    global times
    fig = plt.figure(times+1)
    print('points ',points)
    plt.scatter(points[:, 0], points[:, 1], c='b')
    plotx = []
    ploty = []
    i = 0
    for r in robots:
        plotx.append(r.get_coord()[0])
        ploty.append(r.get_coord()[1])
        plt.annotate(s=i, xy=(r.get_coord()[0], r.get_coord()[1]), xytext=(-5, 5), textcoords='offset points')
        plt.annotate(s=i, xy=(points[i, 0], points[i, 1]), xytext=(-5, 5), textcoords='offset points')
        i = (i + 1) % len(robots)

#    plt.subplot('21' + times.__str__())
#     plt.title('num = num,NO coord , epoch 500, NO edge ')
    plt.scatter(plotx, ploty, c='r')
    plt.plot(20, 20, 'b')
    plt.plot(0, 0, 'b')
    # line
    # lines = open("parent.npy", "r")
    # for line in lines:
    #     s = line.split()
    #     if s[1] == '-1' and s[2] == '-1':
    #         continue
    #     x1 = float(robots[int(s[0])].get_coord()[0])
    #     y1 = float(robots[int(s[0])].get_coord()[1])
    #     x2 = float(robots[int(s[1])].get_coord()[0])
    #     y2 = float(robots[int(s[1])].get_coord()[1])
    #     x3 = float(robots[int(s[2])].get_coord()[0])
    #     y3 = float(robots[int(s[2])].get_coord()[1])
    #     plt.plot([x1, x2], [y1, y2], c='b')
    #     plt.plot([x1, x3], [y1, y3], c='b')
    times = times + 1
    print('times is:', times)


def show3d(points, robots):
    global times
    fig = plt.figure(times)
    ax = Axes3D(fig)
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=20, c='b')
    ax.scatter(points[:, 0], points[:, 1], 0,s=20, c='b')
    plotx = []
    ploty = []
    plotz = []
    # i = 0
    for i, r in enumerate(robots):
        plotx.append(r.get_coord()[0])
        ploty.append(r.get_coord()[1])
        plotz.append(r.z)
        ax.text(r.get_coord()[0], r.get_coord()[1], r.z, i.__str__())
        ax.text(points[i, 0], points[i, 1], 0, i.__str__() + '\'')
        ax.text(points[i, 0], points[i, 1], points[i, 2], i)
        # i = (i + 1) % (len(robots)+1)
    ax.scatter(plotx, ploty, plotz, s=20, c='r')
    ax.scatter(16, 16, 5, s=2, c='b')
    ax.scatter(0, 0, -2, s=2, c='b')

    X = np.arange(-2, 16, 0.1)
    Y = np.arange(-4, 16, 0.1)
    Z = np.zeros((1, len(X)))
    X, Y = np.meshgrid(X, Y)  # XY平面的网格数据
    ax.plot_surface(X, Y, Z, rstride=8, cstride=8,color='y', alpha=0.3)
    times = times + 1
    print('times is:',times)


def anim(list_points):
    fig = plt.figure()
    ax = plt.axes(xlim=(-2, 30), ylim=(-2, 30))
    length = len(list_points)
    new_points = np.array(list_points[0])
    x = np.linspace(6, 20, 1000)
    y = 10*((x-6)/15)**2 + 6
    x2 = np.linspace(12, 28, 1000)
    y2 = 10*(x/15)**2 + 12
    x3 = np.linspace(0, 10, 1000) + 9
    y3 = 10 * np.sin(2 * math.pi * x / 40) + 6
    plt.plot(x, y, color="b", linewidth=2)
    scat = ax.scatter(new_points[:, 0], new_points[:, 1], c='r')

    def update(frame_number):
        global new_points
        new_points = np.array(list_points[frame_number])
        new_points = new_points[:,0:2]
        print('update ', frame_number, list_points[frame_number])
        scat.set_offsets(new_points)
        # for index in range(len(points)):
        #     scattext[index].set_position((new_points[index][0], new_points[index][1]))
        return scat,

    animate2 = animation.FuncAnimation(fig, update, frames=length, interval=200, blit=False)  # interval是每隔70毫秒更新一次，可以查看help
    # Writer = animation.writers['ffmpeg']
    # animate2.save('basic_animation2.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
    animate2.save('function_pointmoving3.gif', writer='imagemagick', fps=30)
    plt.show()



def set_real_position(robots, localization_Nodes):
    cal_nodes = 0
    for index in range(len(robots)):
        if robots[index].isBeacon == False:
            robots[index].isFinalPos = False
        else:
            robots[index].isFinalPos = True
    print('real_position: localizationNodes is ', localization_Nodes)
    while cal_nodes < localization_Nodes:
        for index in range(len(robots)):
            if robots[index].isBeacon == True:
                continue
            if robots[index].isFinalPos == True:
                continue
            print('index %d come to calculate, cal_nodes is %d  '% (index, cal_nodes))
            p1 = robots[index].parent1
            p2 = robots[index].parent2
            if(p1 != -1 and p2 != -1 and robots[p1].isFinalPos == True and robots[p2].isFinalPos == True):
                ix, iy = robots[index].get_coord()
                p1x, p1y = robots[p1].get_coord()
                p2x, p2y = robots[p2].get_coord()
                dis1 = robots[index].dic_neighbors[p1]
                dis2 = robots[index].dic_neighbors[p2]
                def my_solve(paramter):
                    x, y = paramter[0], paramter[1]
                    return [
                        (x - p1x) ** 2 + (y - p1y) ** 2 - dis1 ** 2,
                        (x - p2x) ** 2 + (y - p2y) ** 2 - dis2 ** 2]
                sol = np.real(fsolve(my_solve, np.array([ix, iy]), xtol=1e-3))
                print('fsolve index ',index,sol)
                robots[index].set_coord(sol[0], sol[1])
                robots[index].isFinalPos = True
                cal_nodes = cal_nodes + 1



