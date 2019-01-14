

import numpy as np
import matplotlib.pyplot as plt 
import copy
import os
from config import *
#调用MDS_MAP即可
def cal_dist( Z,limit = np.inf, anchor_num = 0 ):
    """求各个节点对的距离
    每行都代表一个点
    Z:n*m,代表有n个m维的点"""
    Z = np.array( Z, dtype = np.float64 )
    
    n = Z.shape[ 0 ]
    dist = np.zeros( ( n, n ) )
    for i in range( n ):
        for j in range( n ):
            dist[ i ][ j ] = np.sqrt( np.sum( ( Z[ i, : ] - Z[ j, :] ) ** 2 ) )
            
            if i < anchor_num and j < anchor_num:
                continue
            if dist[ i ][ j ] > limit:
                dist[ i ][ j ] = np.inf
    
    return dist

def square_random_nodes( L, num ):
    return np.random.randint( -L, L, size = ( num, 2 ) )
    
def floyed( edges ):
    """求所有节点对的最短距离
    edges为邻接矩阵"""
    dis = np.array( edges, dtype = np.float64 )
    n = dis.shape[ 0 ]
    
    for temp in range( n ):
        for row in range( n ):
            for col in range( n ):
                dis[ row][ col ] = np.min( [ dis[ row ][ col ], dis[ row ][ temp ] + dis[ temp ][ col ] ] )
                
    
    return dis
def MDS( dis, q = 2 ):
    """MDS将dis降成q维
    dis是距离矩阵
    d是想降的维度"""
    n = dis.shape[ 0 ]
    J = np.eye( n ) - np.ones( ( n, n ) ) / n
    
    B = -1/2 * np.matmul( np.matmul( J, dis ** 2 ), J ) 
    
    V, s, T = np.linalg.svd( B )
    T = T.transpose( )
    S = np.zeros( ( n, n) )
    
    for i in range( len( s ) ):
        S[ i ][ i ] = s[ i ]
        
    X = np.matmul( T , np.sqrt( S ) )
    
    rela_map = X[:, 0:q ] 
    
    return rela_map

def my_plot( true, ass ):
    """画图"""
    f = plt.figure( )
    plt.scatter( true[:,0], true[:,1], marker = '+', color = 'c' )
    plt.scatter( ass[:, 0], ass[:,1], marker = 'o', color = 'r' )
    plt.legend( ['True Position', 'Located Position'])
    plt.show( )
    plt.savefig('mds-map.png')

def relative_to_abs( rela_map, true_nodes, anchor_num ):
    """将相对图转换为绝对图"""
    anc_rela_map = np.array( rela_map, dtype = np.float64 )[ 0:anchor_num, : ]
    anc_true_nodes = np.array( true_nodes, dtype = np.float64 )[ 0:anchor_num, : ]
    
    temp = np.hstack( (anc_rela_map, np.ones( (anchor_num, 1 ) ) ) )
    x =  np.linalg.lstsq( temp, anc_true_nodes )
    
    temp = np.hstack( (rela_map, np.ones( ( rela_map.shape[ 0 ], 1 ) ) ) )
    print( type( temp ) )
    res = np.matmul( temp, x[ 0 ])
    
    return res 

def MDS_MAP( edges, anchor_num, points ):
    """MDS_MAP定位算法
    edges是邻接矩阵，最好任意anchor node之间都是有边的
    anchor_num是anchor node的数量
    points是点的真实位置,为n*2矩阵，代表有n个平面点，前anchor_num为anchor node"""
    dist = floyed( edges )
    # print('np.sum(dist == np.inf) is ', np.sum(dist == np.inf))
    for index, dis in enumerate(dist):
        print('np.sum(dis == np.inf)', np.sum(dis == np.inf), len(dis), index)
        if np.sum(dis == np.inf) == len(dis)-1:
            print('dis[0] is np.inf')
            print('dis is ', dis, index)
    
    if( np.sum( dist == np.inf ) > 0 ):
        print( 'don\'t connect' )

        return None
    
    rela_map = MDS( dist )
    abs_map = relative_to_abs( rela_map, points, anchor_num )
    
    return abs_map

def test( ):
    """测试MDS_MAP"""
    square_L = 20
    all_nodes_num = 20
    anchor_num = 5
    limit = 25
    #随机产生点
    # points = square_random_nodes( square_L, all_nodes_num )
    points = np.loadtxt(os.path.join(folder, random_node_filename))
    points = points[:, 0:2]
    list = np.loadtxt(os.path.join(folder, beacon_node_filename))
    limit = list[len(list)-1]
    Beacon1List = np.array(list[0:len(list)-1], dtype=int)
    anchor_num = len(Beacon1List)

    #产生邻接表
    edges = cal_dist( points, limit, anchor_num )
    
    
    abs_map =  MDS_MAP( edges, anchor_num, points )
    print(abs_map)
    rmsd = (1/len(points) * np.sum(np.sqrt((abs_map[:, 0] - points[:, 0])**2 + (abs_map[:, 1] - points[:, 1])**2)))**0.5
    print('rmsd is = ',rmsd)
    my_plot( points, abs_map )


if __name__ == '__main__':
    test( )
    # point = [ [1,2], [3,4]]
    # point[[0,1]] = point[[[1,2], 0]]
    # print('points is ', point)