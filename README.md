# paper code


## 1. execute ./data/create_nodes.py
        you need to create random node to folder : /data/{}/**.npy
        random_nodes.npy: every line shows the node's position
        beacon_nodes.npy: n-1 lines show the beacon position, and the last line shows the communication distance in this network

## 2. execute ./initPos.py
        Use dv_distance algorithm to create dv_distance.npy. In this file, every line shows the node's estimate position by dv-distance
        execute visualization.py compare_random_dvdistance_picture(), you can create the picture "result_random_dvdistance.pdf"

## 3. execute ./main.py
