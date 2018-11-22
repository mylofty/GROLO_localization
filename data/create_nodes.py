import numpy as np
import random
import matplotlib.pyplot as plt


def create_map(nodeNum, mapSize):
    '''
    create a size x size map, and nodeNum random created!
    :param nodeNum:
    :param mapSize:
    :return:
    '''
    random.seed(15)
    lx = list(range(mapSize* 10))
    ly = list(range(mapSize* 10))
    random.shuffle(lx)
    random.shuffle(ly)
    lx = lx[0: nodeNum]
    ly = ly[0: nodeNum]
    arr = np.append(np.divide(lx, 10), np.divide(ly, 10)).reshape((nodeNum, 2))
    lz = [0 for i in range(nodeNum)]
    arr= np.column_stack((arr, lz))
    plt.scatter(arr[:, 0], arr[:, 1], c='b')
    np.savetxt('random_nodes.npy', arr)
    for i in range(nodeNum):
        plt.annotate(s=i, xy=(arr[i, 0], arr[i, 1]), xytext=(-5, 5), textcoords='offset points')
    plt.show()


if __name__ == '__main__':
    create_map(50, 100)
