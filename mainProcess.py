from hexapodRobot import *
from GlobalDebug import *
from D3_TE import *
from dv_distance import *



communication_distance = 0

def cmp_by_value(lhs):
    return lhs[1]


def create_network_topology():
    global communication_distance
    points = np.loadtxt('data/node.npy')
    beacon_dis = np.loadtxt('data/beacon_dis.npy')
    Robot_Num = points.shape[0]
    communication_distance = beacon_dis[len(beacon_dis)-1]
    print('communication_distance', communication_distance)
    robots = [Robot(identity=x, epoch=50, lrn=0.02) for x in range(Robot_Num)]
    Beacon = np.array(beacon_dis[0: len(beacon_dis)-1], dtype=int)
    for index in Beacon:
        robots[index].setBeacon(points[index])
    # calculate the neighbor and sorted
    for i in range(Robot_Num):
        for j in range(i+1, Robot_Num):
            tempDistance = np.sqrt( (points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2
                                    + (points[i][2] - points[j][2])**2)
            if tempDistance < communication_distance:
                robots[i].myNeighbor.append([j, tempDistance])
                robots[j].myNeighbor.append([i, tempDistance])
    for r in robots:
        r.myNeighbor = sorted(r.myNeighbor, key=cmp_by_value)
        # robots move in Z, up and down.
        r.nei_id = []
        r.nei_pos = []
        for nei in r.myNeighbor:
            rid = r.id
            nid = nei[0]
            r.nei_id.append(nid)
            r.nei_pos.append(robots[nid].get_coord())
            r.measured_distance[nid] = np.sqrt((points[rid][0]-points[nid][0])**2 +
                    (points[rid][1]-points[nid][1])**2 +
                    (points[rid][2]+r.t-points[nid][2])**2 )

    # debug print
    for r in robots:
        s = ""
        for t in r.myNeighbor:
            s = s + "%d "%t[0]
        print("Robot%d have neighbor %s"%(r.id, s))
        print("Robot measured_distance", r.measured_distance)
        print("Robot%d neighbor's coord is "%(r.id), r.nei_pos)

    return points, robots

def get_new_topology(points, robots):
    # calculate the neighbor and
    Robot_Num = len(robots)
    global communication_distance
    for i in range(Robot_Num):
        for j in range(i+1, Robot_Num):
            tempDistance = np.sqrt( (points[i][0] - points[j][0])**2 + (points[i][1] - points[j][1])**2
                                    + (points[i][2] - points[j][2])**2)
            if tempDistance < communication_distance:
                robots[i].myNeighbor.append([j, tempDistance])
                robots[j].myNeighbor.append([i, tempDistance])
    for r in robots:
        r.myNeighbor = sorted(r.myNeighbor, key=cmp_by_value)
        # robots move in Z, up and down.
        r.nei_id = []
        for nei in r.myNeighbor:
            rid = r.id
            nid = nei[0]
            r.nei_id.append(nid)
            r.measured_distance[nid] = np.sqrt((points[rid][0]-points[nid][0])**2 +
                    (points[rid][1]-points[nid][1])**2 +
                    (points[rid][2]+r.t-points[nid][2])**2 )


def set_real_position(robots, localization_Nodes):
    cal_nodes = 0
    for index in range(len(robots)):
        if robots[index].isBeacon == False:
            robots[index].isFinalPos = False
        else:
            robots[index].isFinalPos = True
    print('real_position: localizationNodes is ', localization_Nodes)
    while cal_nodes < localization_Nodes:
        for index in range(len(robots)):
            if robots[index].isBeacon == True:
                continue
            if robots[index].isFinalPos == True:
                continue
            print('index %d come to calculate, cal_nodes is %d  '% (index, cal_nodes))
            p1 = robots[index].parent1
            p2 = robots[index].parent2
            if(p1 != -1 and p2 != -1 and robots[p1].isFinalPos == True and robots[p2].isFinalPos == True):
                ix, iy = robots[index].get_coord()
                p1x, p1y = robots[p1].get_coord()
                p2x, p2y = robots[p2].get_coord()
                dis1 = robots[index].d2_distances[p1]
                dis2 = robots[index].d2_distances[p2]
                def my_solve(paramter):
                    x, y = paramter[0], paramter[1]
                    return [
                        (x - p1x) ** 2 + (y - p1y) ** 2 - dis1 ** 2,
                        (x - p2x) ** 2 + (y - p2y) ** 2 - dis2 ** 2]
                sol = np.real(fsolve(my_solve, np.array([ix, iy]), xtol=1e-3))
                print('fsolve index ',index,sol)
                robots[index].set_coord(sol[0], sol[1])
                robots[index].isFinalPos = True
                cal_nodes = cal_nodes + 1


def localization_ontime(robots, flexibleNum, epochs=200):
    robot_num = len(robots)
    i = 0
    for epoch in range(epochs+1):
        print("epoch %d:------------------------------------------------" % epoch)
        # i = np.random.randint(0, robot_num)
        nei_dis = [value for value in robots[i].d2_distances.values()]
        nei_pos = [robots[key].get_coord() for key in robots[i].d2_distances.keys()]

        if epoch > 2 and (epoch == epochs):
            set_real_position(robots, robot_num - flexibleNum-3)
            continue
        print('localization_ontime robot',i)
        robots[i].run(nei_pos=nei_pos, nei_dis=nei_dis)
        print("robots[%d].coord: " % i, robots[i].get_coord())
        i = i + 1
        if (i >= robot_num):
            i = 0
    # robots[5].show_loss_curve()
    # show(points, robots)


def Test_D3_TE():
    points, robots = create_network_topology()
    parentList, distanceList, zList,flexibleNum = from_3D_to_2D(robots)
    print('parentList',parentList)
    print('ZList is', zList)
    print('distanceList',distanceList)



def center_main():         # the center nodes . write all the robots to database
    points, robots = create_network_topology()
    parentList, distanceList, zList, flexibleNum = from_3D_to_2D(robots)  # calculate Z, and finish triangle extension
    setInitial(robots)  # estimate the robots' coord(x,y)
    for r in robots:
        write_to_db(r)
    # localization_ontime(robots, flexibleNum, 5)
    show(points, robots)


def distribute_main():
    current_robot = 8
    robots = Robot(identity=current_robot, epoch=50, lrn=0.02)
    write_to_db(robots[current_robot])
    read_from_db(robots[current_robot])
    print('the robot parent is %d %d, state is %d' % (robots[current_robot].parent1, robots[current_robot].parent2, robots[current_robot].state))


if __name__ == '__main__':
    center_main()
    # distribute_main()

