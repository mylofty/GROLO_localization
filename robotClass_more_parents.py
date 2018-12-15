
import numpy as np
from matplotlib import pyplot as plt
from triangle_extension_file_more_parents import triangle_extension


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
        self.parent1 = []
        self.parent2 = []
        self.root1 = []
        self.root2 = []
        self.query1 = []
        self.query2 = []

    def add_parents(self, p1, p2):
        self.parent1.append(p1)
        self.parent2.append(p2)

    def add_roots(self, r1, r2):
        self.root1.append(r1)
        self.root2.append(r2)

    def is_child_of_id(self, other):
        for p in self.parent1:
            if p==other:
                return True
        for p in self.parent2:
            if p==other:
                return True
        return False

    def has_same_root(self, other):
        for i in range(len(self.root1)):
            for j in range(len(other.root1)):
                if self.root1[i]==other.root1[j] and self.root2[i]==other.root2[j] or \
                    self.root1[i]==other.root2[j] and self.root2[i]==other.root1[j]:
                    return True
        return False

    def has_same_root_but_not_parents(self, other):
        for i in range(len(self.root1)):
            for j in range(len(other.root1)):
                if self.root1[i]==other.root1[j] and self.root2[i]==other.root2[j] or \
                    self.root1[i]==other.root2[j] and self.root2[i]==other.root1[j]:
                    if other.id!=self.parent1[i] and other.id!=self.parent2[i]:
                        return True
        return False

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
        coord, loss = psolver.solver(self.coord, neighbors, dists)
        print('loss is ', loss)
        self.set_coord(coord)
        self.loss_dump.append(loss)

    def show_loss_curve(self):
        plt.figure(10)
        print('loss_dump is', self.loss_dump)
        length = len(self.loss_dump)
        print('curve length is ',length)
        plt.annotate(s=round(self.loss_dump[length-1], 2), xy=((length-1)*self.epoch, self.loss_dump[length-1]), xytext=(-5, 5),
                     textcoords='offset points')
        # plt.annotate(s=round(self.loss_dump[length - 2], 2), xy=((length - 2)*self.epoch, self.loss_dump[length - 2]), xytext=(-5, 5),
        #              textcoords='offset points')
        plt.plot(np.arange(0,length,step=1)*self.epoch, self.loss_dump)
        np.savetxt('./loss_dump2.txt',np.array(self.loss_dump))
        plt.show()
