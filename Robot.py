import tensorflow as tf
import numpy as np

from matplotlib import pyplot as plt
from triangle_extension_file import triangle_extension


class TD_Robot(object):
    def __init__(self, rid):
        self.id = rid

        self.state = 0
        self.parent1 = -1
        self.parent2 = -1
        self.root1 = -1
        self.root2 = -1
        self.extra = -1
        self.query1 = -1
        self.query2 = -1

        self.myNeighbor = []

        self.is_beacon = False

        self.x = None
        self.y = None
        self.z = None

        self.t = None
        self.measured_distances = {}
        self._2d_distances = {}

        pass

    def distance_to(self, rid):
        for nei in self.myNeighbor:
            if nei[0]==rid:
                return nei[1]

    def cal_z(self, probot):

        if self.is_beacon or self.z :
            return self.z

        for nei in self.myNeighbor :
            if probot[nei[0]].z!=None :

                d1 = nei[1]
                d2 = self.measured_distances[nei[0]]

                print(d1, d2)

                self.z = (d2**2-d1**2+2*probot[nei[0]].z*self.t-self.t**2)/(2*self.t)

                print(self.z)

                return self.z

    def cal_2d_distances(self, probot):
        if self.z==None:
            return

        for nei in self.myNeighbor :
            if probot[nei[0]].z!=None:
                tmp = (nei[1]**2-(self.z-probot[nei[0]].z)**2)**0.5
                self._2d_distances[nei[0]] = tmp
                # nei[1] = tmp



    def triangle_extension(self, probot):
        triangle_extension(self, probot)

    def set_beacon(self, coord):
        self.is_beacon = True
        self.state = 3
        self.root1 = self.root2 = self.id

        self.x, self.y, self.z = coord

    def get_coord(self):
        return self.x, self.y, self.z



def from_3D_to_2D(nodes):
    print('from_3D_to_2D points is ')
    print(nodes)

    def read3array(pointX, pointY, pointZ):
    
        for i, point in enumerate(nodes):
            pointX[i] = point[0]
            pointY[i] = point[1]
            pointZ[i] = point[2]

        pass

    def cmp_by_value(lhs):
        return lhs[1]

    def createMap(probot):
        pointX = [0 for i in range(RobotNum)]
        pointY = [0 for i in range(RobotNum)]
        pointZ = [0 for i in range(RobotNum)]

        read3array(pointX, pointY, pointZ)

        for i in range(RobotNum):
            for j in range(i+1,RobotNum):
                tempDistance = np.sqrt( (nodes[i][0]-nodes[j][0])**2 + (nodes[i][1]-nodes[j][1])**2 +
                    (nodes[i][2]-nodes[j][2])**2 )
                if(tempDistance<Distance):
                    probot[i].myNeighbor.append([j, tempDistance])
                    probot[j].myNeighbor.append([i, tempDistance])

        for r in probot:
            r.myNeighbor = sorted(r.myNeighbor, key=cmp_by_value)

        for r in probot:
            s = ""
            for t in r.myNeighbor:
                s = s + "%d "%t[0]
            print("Robot%d have neighbor %s"%(r.id, s))

    def measure(probot):
        for r in probot:
            rid = r.id
            for nei in r.myNeighbor:
                nid = nei[0]
                r.t = -2
                r.measured_distances[nid] = np.sqrt((nodes[rid][0]-nodes[nid][0])**2 +
                    (nodes[rid][1]-nodes[nid][1])**2 +
                    (nodes[rid][2]+r.t-nodes[nid][2])**2 )
            # print(rid, r.measured_distances)
        pass

    # nodes = np.loadtxt("./node.npy")

    RobotNum = len(nodes)
    # Distance = 28
    # #random test
    # Beacon1ID = 17
    # Beacon2ID = 45
    # Beacon3ID = 26
    list = np.loadtxt('beacon_dis.npy')
    Distance = list[len(list)-1]

    beacons = np.array(list[0:len(list)-1], dtype=int)

    probot = [TD_Robot(i) for i in range(RobotNum)]

    createMap(probot)
    measure(probot)

    for bid in beacons:
        probot[bid].set_beacon(nodes[bid])

    count = 30

    flexiblecount = 0
    localization = 0
    rigidnum = 0
    flag0 = True
    for count_ in range(count):
        for i, r in enumerate(probot):

            print("this is robot %d"%i)

            r.cal_z(probot)
            r.cal_2d_distances(probot)
            r.triangle_extension(probot)



            for i in range(RobotNum):
                if probot[i].state==0:
                    flexiblecount +=1
            print("flexible robot have %d"%flexiblecount)
            flexiblecount = 0

            for i in range(RobotNum) :
                if probot[i].state==2:
                    localization += 1

            print("localization robot have %d"%localization)
            localization = 0

            for i in range(RobotNum):
                if probot[i].state==1:
                    rigidnum += 1

            print("rigid robot have %d"%rigidnum)
            rigidnum = 0




    with open("parent.npy","w") as parentnpy:
        for r in probot:
            parentnpy.write("%d %d %d\n"%(r.id, r.parent1, r.parent2))


    # for r in probot:
    #     print(r._2d_distances)

    print("-----------------------")

    for r in probot:
        dic = {}
        for n in r.myNeighbor:
            dic[n[0]] = ((nodes[r.id][0]-nodes[n[0]][0])**2 + (nodes[r.id][1]-nodes[n[0]][1])**2)**0.5

        # print(dic)


    with open("distance.npy","w") as distancenpy :
        for r in probot :
            for i in range(RobotNum) :
                if i==r.id:
                    distancenpy.write("0 ")
                    continue

                distancenpy.write(str(r._2d_distances[i]) if i in r._2d_distances else str(999))
                distancenpy.write(' ')
            distancenpy.write("\n")

    parentList = []
    distanceList = []
    zList = []

    for r in probot:
        parentList.append([r.id, r.parent1, r.parent2])
        distanceList.append([r._2d_distances[i] if i in r._2d_distances else 999 for i in range(RobotNum)])
        zList.append(r.z)
    # print(zList)
    print('parentList',parentList)
    print('ZList is', zList)
    print('distanceList',distanceList)
    return parentList, distanceList, zList



if __name__=="__main__":
    nodes = np.loadtxt("./node2.npy")
    print('node2 shape is',nodes.shape)
    from_3D_to_2D(nodes)




