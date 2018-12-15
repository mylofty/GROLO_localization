import numpy as np
import random
import matplotlib.pyplot as plt
import os
from config import *
from mpl_toolkits.mplot3d import Axes3D

picture_folder = os.path.join(folder, 'img')
if not os.path.exists(picture_folder):
    os.mkdir(picture_folder)


def compare_random_dvdistance_picture(folder=folder, random_node_filename = random_node_filename,
                                      beacon_node_filename = beacon_node_filename, dv_distance_result = dv_distance_result):
    '''
    create a picture to show random_nodes and dv_distance_nodes
    :param folder:  the whole data folder
    :param random_node_filename:
    :param beacon_node_filename:
    :return:
    '''
    plt.figure(figsize=(8, 6))
    plt.title('compare: dv_distance')
    list = np.loadtxt(os.path.join(folder, beacon_node_filename))
    Beacon1List = np.array(list[0:len(list)-1], dtype=int)
    old = np.loadtxt(os.path.join(folder, random_node_filename))
    new = np.loadtxt(os.path.join(folder, dv_distance_result))
    plt.xlim(-2, 110)
    plt.ylim(-2, 110)
    labelB = False
    labelN = False
    labelE = False

    for index in range(len(old)):
        if index not in Beacon1List:
            if labelN == False:
                # ,edgecolors='g',edgecolors='b',,
                plt.scatter(old[index, 0], old[index, 1], c='', edgecolors='b', marker='o', s=60, label = 'real position')
                labelN = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='', edgecolors='b', marker='o', s=60)
            # # estimated nodes
            if labelE == False:
                plt.scatter(new[index, 0], new[index, 1], c='r', marker='+', s=60, label='estimated position')
                labelE = True
            else:
                plt.scatter(new[index, 0], new[index, 1], c='r', marker='+', s=60)
        # Beacon
        else:
            if labelB == False:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100, label='beacon')
                labelB = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100)
    # show label
    for i in range(len(old)):
        plt.annotate(s=i, xy=(old[i, 0], old[i, 1]), xytext=(-5, 5), textcoords='offset points')
        plt.annotate(s=i, xy=(new[i, 0], new[i, 1]), xytext=(-5, 5), textcoords='offset points')


    rmsd = (1/len(old) * np.sum(np.sqrt((new[:, 0] - old[:, 0])**2 + (new[:, 1] - old[:, 1])**2)))**0.5
    print('dv-distance rmsd is = ', rmsd)
    plt.legend()
    plt.savefig(os.path.join(picture_folder, "result_random_dvdistance.pdf"))
    plt.show()


def compare_random_Gradient_picture(folder = folder, random_node_filename = random_node_filename,
                                    GradientDescent_node_filename = gradient_descent_result):
    '''
    compare origin position with GradientDescent's position
    :param folder:
    :param random_node_filename:
    :param GradientDescent_node_filename:
    :return:
    '''
    plt.figure(figsize=(8, 6))
    plt.title('compare: gradient_descent')
    list = np.loadtxt(os.path.join(folder, beacon_node_filename))
    Beacon1List = np.array(list[0:len(list)-1], dtype=int)
    old = np.loadtxt(os.path.join(folder, random_node_filename))
    new = np.loadtxt(os.path.join(folder, GradientDescent_node_filename))
    plt.xlim(-2, 110)
    plt.ylim(-2, 110)
    labelB = False
    labelN = False
    labelE = False

    for index in range(len(old)):
        if index not in Beacon1List:
            if labelN == False:
                # ,edgecolors='g',edgecolors='b',,
                plt.scatter(old[index, 0], old[index, 1], c='', edgecolors='b', marker='o', s=60, label = 'real position')
                labelN = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='', edgecolors='b', marker='o', s=60)
            # # estimated nodes
            if labelE == False:
                plt.scatter(new[index, 0], new[index, 1], c='r', marker='+', s=60, label='estimated position')
                labelE = True
            else:
                plt.scatter(new[index, 0], new[index, 1], c='r', marker='+', s=60)
        # Beacon
        else:
            if labelB == False:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100, label='beacon')
                labelB = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100)
    # show label
    for i in range(len(old)):
        plt.annotate(s=i, xy=(old[i, 0], old[i, 1]), xytext=(-5, 5), textcoords='offset points')
        # plt.annotate(s=i, xy=(new[i, 0], new[i, 1]), xytext=(-5, 5), textcoords='offset points')


    rmsd = (1/len(old) * np.sum(np.sqrt((new[:, 0] - old[:, 0])**2 + (new[:, 1] - old[:, 1])**2)))**0.5
    print('Gradient descent rmsd is = ', rmsd)
    plt.legend()
    plt.savefig(os.path.join(picture_folder, "result_random_gradient.pdf"))
    plt.show()


def compare_random_GROLO_picture(folder = folder, random_node_filename = random_node_filename,
                                 GROLO_node_filename = GROLO_result):
    '''
    compare origin nodes position with GROLO localization position
    :param folder:
    :param random_node_filename:
    :param GROLO_node_filename:
    :return:
    '''
    plt.figure(figsize=(8, 6))
    plt.title('compare: GROLO')
    list = np.loadtxt(os.path.join(folder, beacon_node_filename))
    Beacon1List = np.array(list[0:len(list)-1], dtype=int)
    old = np.loadtxt(os.path.join(folder, random_node_filename))
    new = np.loadtxt(os.path.join(folder, GROLO_node_filename))
    plt.xlim(-2, 110)
    plt.ylim(-2, 110)
    labelB = False
    labelN = False
    labelE = False

    for index in range(len(old)):
        if index not in Beacon1List:
            if labelN == False:
                # ,edgecolors='g',edgecolors='b',,
                plt.scatter(old[index, 0], old[index, 1], c='', edgecolors='b', marker='o', s=60, label = 'real position')
                labelN = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='', edgecolors='b', marker='o', s=60)
            # # estimated nodes
            if labelE == False:
                plt.scatter(new[index, 0], new[index, 1], c='r', marker='+', s=60, label='estimated position')
                labelE = True
            else:
                plt.scatter(new[index, 0], new[index, 1], c='r', marker='+', s=60)
        # Beacon
        else:
            if labelB == False:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100, label='beacon')
                labelB = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100)
    # show label
    for i in range(len(old)):
        plt.annotate(s=i, xy=(old[i, 0], old[i, 1]), xytext=(-5, 5), textcoords='offset points')
        # plt.annotate(s=i, xy=(new[i, 0], new[i, 1]), xytext=(-5, 5), textcoords='offset points')


    rmsd = (1/len(old) * np.sum(np.sqrt((new[:, 0] - old[:, 0])**2 + (new[:, 1] - old[:, 1])**2)))**0.5
    print('random and GROLO rmsd is = ', rmsd)
    plt.legend()
    plt.savefig(os.path.join(picture_folder, "result_random_GROLO.pdf"))
    plt.show()



def TExtension_picture(folder = folder, random_node_filename = random_node_filename,
                       TE_parent_filename = TE_parent_filename):
    plt.figure(figsize=(8, 6))
    list = np.loadtxt(os.path.join(folder, beacon_node_filename))
    Beacon1List = np.array(list[0:len(list)-1], dtype=int)
    # ./Testdata/nodes_50_beacon_3/
    old = np.loadtxt(os.path.join(folder, random_node_filename))
    # ./Testdata/nodes_100_beacon_5_25/
    # new = np.loadtxt('gradient_descent.npy')
    # new = np.loadtxt(os.path.join(folder, 'forecast_position.npy'))
    # new = np.loadtxt('dv_distance.npy')
    parent = np.loadtxt(os.path.join(folder, TE_parent_filename))
    # plt.title('nodes\' number is 150 \nglobal node is 147,beacon is 12,49,60 ')
    plt.xlim(-2, 110)
    plt.ylim(-2, 110)
    labelB = False
    labelN = False
    labelE = False

    # line
    for index in range(len(parent)):
        if index not in Beacon1List and parent[index, 1] != -1 and parent[index, 2] != -1:
            plt.plot([old[int(parent[index,0]), 0], old[int(parent[index, 1]), 0] ], [old[int(parent[index, 0]), 1], old[int(parent[index,1]), 1]],c='b')# #808080
            plt.plot([old[int(parent[index,0]), 0], old[int(parent[index, 2]), 0] ], [old[int(parent[index, 0]), 1], old[int(parent[index,2]), 1]],c='b')

    for index in range(len(old)):
        if index not in Beacon1List:
            if labelN == False:
                # ,edgecolors='g',edgecolors='b',,
                plt.scatter(old[index, 0], old[index, 1], c='b',edgecolors='b', marker='.', s=60, label = 'real position')
                labelN = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='b',edgecolors='b', marker='.', s=60)

        # Beacon
        else:
            if labelB == False:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100, label='beacon')
                labelB = True
            else:
                plt.scatter(old[index, 0], old[index, 1], c='r', marker='v', s=100)
    # # show label
    # for i in range(len(old)):
    #     plt.annotate(s=i, xy=(old[i, 0], old[i, 1]), xytext=(-5, 5), textcoords='offset points')
    plt.legend()
    plt.savefig(os.path.join(picture_folder, "result_TE.pdf"))
    plt.show()


if __name__ == '__main__':
    compare_random_dvdistance_picture()
    compare_random_Gradient_picture()
    # TExtension_picture()
    compare_random_GROLO_picture()

