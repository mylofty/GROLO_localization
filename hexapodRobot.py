import tensorflow as tf
import copy
import numpy as np
from class_achieve import *
from triangle_extension_file import triangle_extension


class Robot(object):
    def __init__(self, identity, epoch, lrn):
        self.id = identity
        # tensorflow GD
        self.sess = tf.Session()
        self.coord = tf.Variable(tf.truncated_normal(shape=(2,), mean=5, stddev=1))
        # all the neighbors of this robots, depends on neighbor message
        self.neighborsCoord = tf.placeholder(tf.float32, shape=(None, 2))
        # real distance between the neighbor and the robots, depends on neighbor message
        self.dist_gt = tf.placeholder(tf.float32, shape=(None, ))
        self.dist_ob = tf.map_fn(lambda x: self.distance(self.coord, x), self.neighborsCoord) # estimate distance
        self.losses = tf.square(tf.square(self.dist_gt) - tf.square(self.dist_ob))   # square loss
        self.reduced_loss = tf.reduce_sum(self.losses)
        self.epoch = epoch
        self.optimizer = tf.train.AdamOptimizer(learning_rate=lrn)
        self.train_op = self.optimizer.minimize(self.reduced_loss)
        self.sess.run(tf.global_variables_initializer())
        self.loss_dump = []

        # neighbor message
        self.nei_id = []
        # self.nei_dis = [] # this is 2 dimension
        # self.nei_pos = [] # shape is (,2)

        # triangle extension
        self.state = 0
        self.parent1 = -1
        self.parent2 = -1
        self.root1 = -1
        self.root2 = -1
        self.extra = -1
        self.query1 = -1
        self.query2 = -1

        #calculate Z
        self.myNeighbor = []  #include [nid, neighbor_distance], it has been sorted, 3D
        self.t = -2           # robot move in Z, up and down ,to calculate pos.z
        # self.D3distance = None
        self.measured_distance = {} # after move in Z, new D3distance
        self.d2_distances = {}
        self.z = None

        # formation control
        self.isFinalPos = False
        self.isBeacon = False
        self.centerCoord = [-1, -1]
        self.initCoord = [-1, -1]

    def distance(self, coord1, coord2):
        return tf.sqrt(tf.square(coord1[0] - coord2[0]) + tf.square(coord1[1] - coord2[1]))

    def get_coord(self):
        return self.sess.run(self.coord)

    def set_coord(self, x, y):
        self.sess.run(self.coord.assign([x, y]))

    def getZ(self):
        return self.z

    def setParents(self, p1, p2):
        self.parent1 = p1
        self.parent2 = p2

    def setBeacon(self, coord):
        self.isBeacon = True
        self.set_coord(coord[0], coord[1])
        self.z = 0
        self.state = 3
        self.root1 = self.root2 = self.id

    def triangle_extension(self, probot):
        triangle_extension(self, probot)

    # tensorflow: gradient descent run
    def run(self, nei_pos, nei_dis):
        tensorflow_run(self, nei_pos, nei_dis)



    # calculate Z
    def distance_to(self, rid):
        for nei in self.myNeighbor:
            if nei[0]==rid:
                return nei[1]

    def cal_z(self, robots):
        if self.isBeacon or self.z:
            return self.z
        for nei in self.myNeighbor:
            if robots[nei[0]].z != None:
                d1 = nei[1]
                d2 = self.measured_distance[nei[0]]
                print(d1, d2)
                self.z = (d2**2-d1**2+2*robots[nei[0]].z*self.t-self.t**2)/(2*self.t)
                # print(self.z)
                return self.z

    def cal_2d_distances(self, robots):
        if self.z == None:
            return
        for nei in self.myNeighbor:
            if robots[nei[0]].z != None:
                tmp = (nei[1]**2-(self.z-robots[nei[0]].z)**2)**0.5
                self.d2_distances[nei[0]] = tmp



