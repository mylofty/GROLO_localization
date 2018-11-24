import tensorflow as tf
import math

'''
this is a class for gradient descent use tensorflow
'''
class PositionSolver(object):
    def __init__(self, sess, steps=50, lrn=0.02):
        self.steps = steps
        self.sess = sess
        self.lrn = lrn

        self.coord = tf.Variable(tf.truncated_normal(shape=(2,), mean=5, stddev=1))
        self.neighborsCoord = tf.placeholder(tf.float32, shape=(None, 2))  # neighbor's coord
        self.neighborsDist = tf.placeholder(tf.float32, shape=(None,))
        obtainDist = tf.map_fn(lambda x: self.distance(self.coord, x), self.neighborsCoord)
        self.losses = tf.square(tf.square(self.neighborsDist) - tf.square(obtainDist))
        self.reduced_loss = tf.reduce_sum(self.losses)

        self.optimizer = tf.train.AdamOptimizer(learning_rate=lrn)
        self.train_op = self.optimizer.minimize(self.reduced_loss)
        sess.run(tf.global_variables_initializer())

    def distance(self, t1, t2):
        return tf.sqrt(tf.square(t1[0] - t2[0]) + tf.square(t1[1] - t2[1]))

    def solver(self, initialcoord, neighbors, dists):
        '''
        use this function to get the gradient descent value
        :param initialcoord: the initial position of nodes
        :param neighbors: the nodes's neighbor's position
        :param dists:  the distance between neighbor and the nodes
        :return:
        '''
        self.sess.run(self.coord.assign(initialcoord))

        if neighbors is None or neighbors == []:
            return
        num = len(neighbors)
        nei = []
        dis = []
        for i in range(num):
            nei.append(neighbors[i])
            dis.append(dists[i])
        # print('neighbor coord is', nei)
        # print('nei_dis is ', dis)
        for i in range(self.steps):
            coord, _, loss = self.sess.run([self.coord,
                                            self.train_op,
                                            self.reduced_loss],
                                           feed_dict={
                self.neighborsCoord: nei,
                self.neighborsDist: dis
            })
            # print('[{}]coord is [{}], loss is {}'.format(i, coord, loss))
        return coord, loss


if __name__ == '__main__':
    sess = tf.Session()
    neighborsCoord = [[0, 0], [0, 1], [1, 0]]
    neighborsDist = [math.sqrt(2)/2, math.sqrt(2)/2, math.sqrt(2)/2]
    initialPos = [0.3, 0.6]

    ps = PositionSolver(sess, 50, 0.02)
    coord, loss = ps.solver([0.3, 0.6], neighborsCoord, neighborsDist)
    print('coord[{}], loss {}'.format(coord, loss))
