
import numpy as np

def from_3D_to_2D(robots):
    RobotNum = len(robots)
    count = 20
    flag0 = True
    flexiblecount = 0
    localization = 0
    rigidnum = 0
    for count_ in range(count):
        for i, r in enumerate(robots):

            print("this is robot %d"%i)
            r.cal_z(robots)
            r.cal_2d_distances(robots)
            r.triangle_extension(robots)

        # flexiblecount = 0
        for i in range(RobotNum):
            if robots[i].state==0:
                flexiblecount +=1
        print("flexible robot have %d"%flexiblecount)
        # localization = 0
        for i in range(RobotNum) :
            if robots[i].state==2:
                localization += 1
        print("localization robot have %d"%localization)
        # rigidnum = 0
        for i in range(RobotNum):
            if robots[i].state==1:
                rigidnum += 1
        print("rigid robot have %d"%rigidnum)

    with open("data/parent.npy","w") as parentnpy:
        for r in robots:
            parentnpy.write("%d %d %d\n"%(r.id, r.parent1, r.parent2))

    parentList = []
    distanceList = []
    zList = []
    for r in robots:
        parentList.append([r.id, r.parent1, r.parent2])
        for i in range(len(robots)):
            if i in r.d2_distances:
                distanceList.append(r.d2_distances[i])
            elif i == r.id:
                distanceList.append(0)
            else:
                distanceList.append(999)

        # distanceList.append([r.d2_distances[i] if i in r.d2_distances else if i == r.id 999 for i in range(RobotNum)])
        zList.append(r.z)
    # print(zList)
    distanceList = np.array(distanceList).reshape((RobotNum,RobotNum))
    return parentList, distanceList, zList, flexiblecount


