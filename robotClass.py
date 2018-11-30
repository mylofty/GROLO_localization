import math
import numpy as np
from matplotlib import pyplot as plt
from triangle_extension_file import triangle_extension


class Robot(object):
    def __init__(self, id):
        self.id = id
        self.isBeacon = False
        self.isFinalPos = False
        self.coord = []  # robot's coord [x, y]
        # self.neighborsCoord = []  # neighbor's coord [x, y]

        self.nei_id = []
        self.myNeighbor = []  # this is construct like [id, distance]
        self.measured_distance = {} # this is a map,  key is neighbor's id, value is neighbor's distance

        self.loss_dump = []  # loss curve

        # triangle extension
        self.state = 0
        self.parent1 = -1
        self.parent2 = -1
        self.root1 = -1
        self.root2 = -1
        self.extra = -1
        self.query1 = -1
        self.query2 = -1

    def set_parents(self, p1, p2):
        self.parent1 = p1
        self.parent2 = p2

    def set_beacon(self):
        self.isBeacon = True
        self.state = 3
        self.root1 = self.root2 = self.id

    def get_coord(self):
        return self.coord

    def set_coord(self, coord):
        self.coord = coord

    def distance_to(self, rid):
        for nei in self.myNeighbor:
            if nei[0]==rid:
                return nei[1]

    def triangle_extension(self, probot):
        triangle_extension(self, probot)

    def run(self, psolver, neighbors, dists):
        if(self.isBeacon == True):
            return
        if neighbors is None or neighbors == []:
            return
        # print('neighbor ', neighbors)
        # print('distss ', dists)
        # print('origin coord', self.coord)
        coord, loss = psolver.solver(self.coord, neighbors, dists)
        print('loss is ', loss)
        assert not math.isnan(loss)
        if not math.isnan(coord[0]):
            self.set_coord(coord)
            self.loss_dump.append(loss)

    def show_loss_curve(self):
        plt.figure(10)
        print('loss_dump is', self.loss_dump)
        length = len(self.loss_dump)
        print('curve length is ', length)
        plt.annotate(s=round(self.loss_dump[length-1], 2), xy=((length-1)*self.epoch, self.loss_dump[length-1]), xytext=(-5, 5),
                     textcoords='offset points')
        # plt.annotate(s=round(self.loss_dump[length - 2], 2), xy=((length - 2)*self.epoch, self.loss_dump[length - 2]), xytext=(-5, 5),
        #              textcoords='offset points')
        plt.plot(np.arange(0,length,step=1)*self.epoch, self.loss_dump)
        np.savetxt('./loss_dump2.txt',np.array(self.loss_dump))
        plt.show()
