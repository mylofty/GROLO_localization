# -*- coding: utf-8 -*-
from scipy.optimize import fsolve
import numpy as np
import os
from math import *
from config import *


point_list = np.loadtxt(os.path.join(folder, beacon_node_filename))
Beacon = np.array((point_list[0:len(point_list)-1]), dtype=int)
Distance = point_list[len(point_list)-1]
print('Communication Distance is ', Distance)
print('Beacon is ', Beacon)


class Robot:
    def __init__(self):
        self.posx = -1
        self.posy = -1
        self.isBeacon = False
        self.myNeighbor = []
        self.dv_distance = []


def dv_distance():
    points = np.loadtxt(os.path.join(folder, random_node_filename), dtype=np.float32)
    node_num = len(points)
    robot = [Robot() for i in range(node_num)]
    for index in Beacon:
        robot[index].isBeacon = True
    for index in range(node_num):
        robot[index].posx = points[index, 0]
        robot[index].posy = points[index, 1]
        robot[index].dv_distance = [0] * node_num

    # initial myNeighbor
    for i in range(node_num):
        for j in range(i + 1, node_num):
            tempDistance = np.sqrt(
                (robot[i].posx - robot[j].posx) ** 2 + (robot[i].posy - robot[j].posy) ** 2)
            print('real tempDistance: %d' %i, tempDistance)
            np.random.seed(12345)
            # tempDistance = tempDistance + tempDistance * (np.random.random() * 0.02 - 0.01)  #是否加噪声
            print('get tempDistance:', tempDistance)

            if (tempDistance < Distance):
                robot[i].myNeighbor.append([j, tempDistance])
                robot[j].myNeighbor.append([i, tempDistance])
    # initial dv_distance
    for i in range(node_num):
        for j in range(node_num):
            robot[i].dv_distance[j] = 999
            if i == j:
                robot[i].dv_distance[j] = 0
    for i in range(node_num):
        for j in range(len(robot[i].myNeighbor)):
            nei_id = robot[i].myNeighbor[j][0]
            nei_distance = robot[i].myNeighbor[j][1]
            print('nei_distance', i, nei_id, nei_distance)
            robot[i].dv_distance[nei_id] = nei_distance

    # dv_distance
    for i in range(node_num):
        for j in range(node_num):
            for k in range(node_num):
                if robot[j].dv_distance[k] > robot[j].dv_distance[i] + robot[i].dv_distance[k]:
                    robot[j].dv_distance[k] = robot[j].dv_distance[i] + robot[i].dv_distance[k]

    # print dv_distance
    for i in range(node_num):
        for j in range(node_num):
            print('%.3f' % robot[i].dv_distance[j], end='   ')
        print()
    coordlist = []
    for index in range(node_num):
        if index in Beacon:
            coordlist.append([robot[index].posx, robot[index].posy])
        else:
            beacon_sort = []
            for b in Beacon:
                dis = robot[index].dv_distance[b]
                beacon_sort.append([b, dis])
            beacon_sort = np.array(beacon_sort)
            # print('before sort %d',index, beacon_sort)
            beacon_sort = beacon_sort[np.lexsort(beacon_sort.T)]
            # print('after sort %d',index, beacon_sort)
            dis1 = beacon_sort[0, 1]
            b1x = robot[int(beacon_sort[0, 0])].posx
            b1y = robot[int(beacon_sort[0, 0])].posy
            dis2 = beacon_sort[1, 1]
            b2x = robot[int(beacon_sort[1, 0])].posx
            b2y = robot[int(beacon_sort[1, 0])].posy
            dis3 = beacon_sort[2, 1]
            b3x = robot[int(beacon_sort[2, 0])].posx
            b3y = robot[int(beacon_sort[2, 0])].posy
            if index == 0:
                print('distance with beacon1, beacon2, beacon3: ', dis1, dis2, dis3)
            if dis1 > 900 or dis2 > 900 or dis3 > 900:
                print('node %d can not connect with beacon' % index)
                sol = [-1, -1.1]
            else:
                def function(r):
                    x = r[0]
                    y = r[1]
                    return [
                        2 * (b1x - b2x) * x + 2 * (b1y - b2y) * y - dis2 ** 2 + dis1 ** 2 +
                        b2x ** 2 - b1x ** 2 + b2y ** 2 - b1y ** 2,
                        2 * (b1x - b3x) * x + 2 * (b1y - b3y) * y - dis3 ** 2 + dis1 ** 2 +
                        b3x ** 2 - b1x ** 2 + b3y ** 2 - b1y ** 2
                    ]
                sol = fsolve(function, np.array([1, 1]), xtol=1e-5)

            coordlist.append(sol)
            print('sol', index, sol)
    # print(coordlist)
    np.savetxt(os.path.join(folder, dv_distance_result), coordlist)
    return coordlist


if __name__ == '__main__':
    dv_distance()
