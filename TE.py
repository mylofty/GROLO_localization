import os
import numpy as np
from config import *

def TE_2D(robots):
    RobotNum = len(robots)
    count = 20
    flag0 = True
    flexiblecount = 0
    localization = 0
    rigidnum = 0
    for count_ in range(count):
        for i, r in enumerate(robots):
            print("this is robot %d"%i)
            r.triangle_extension(robots)

    flexiblecount = 0
    for i in range(RobotNum):
        if robots[i].state==0:
            flexiblecount +=1
    print("flexible robot have %d"%flexiblecount)
    localization = 0
    for i in range(RobotNum) :
        if robots[i].state==2:
            localization += 1
    print("localization robot have %d"%localization)
    rigidnum = 0
    for i in range(RobotNum):
        if robots[i].state==1:
            rigidnum += 1
    print("rigid robot have %d"%rigidnum)

    with open(os.path.join(folder, TE_parent_filename),"w") as parentnpy:
        for r in robots:
            parentnpy.write("%d %d %d\n"%(r.id, r.parent1, r.parent2))

    parentList = []
    distanceList = []
    for r in robots:
        parentList.append([r.id, r.parent1, r.parent2])
        for i in range(len(robots)):
            if i in r.measured_distance:
                distanceList.append(r.measured_distance[i])
            elif i == r.id:
                distanceList.append(0)
            else:
                distanceList.append(999)

    distanceList = np.array(distanceList).reshape((RobotNum, RobotNum))
    return parentList, distanceList, flexiblecount


