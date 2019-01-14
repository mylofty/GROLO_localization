
import matplotlib.pyplot as plt

# x = [50, 100, 150, 200, 250, 300, 350, 400]
# beacon_precent_5 = [8.514, 6.624, 4.47, 3.61, 2.11, 1.5, 1.02, 0.8]
# beacon_precent_8 = [8.427, 6.164, 3.4936, 2.268, 1.90, 1.24, 0.85, 0.6]
# beacon_precent_10 = [7.85, 5.901, 2.858, 2.00, 1.62, 0.95, 0.65, 0.5]
#
# plt.figure()
# plt.xlabel('node number')
# plt.ylabel('RMSE')
# plt.plot(x, beacon_precent_5, 'r', marker='o', label='5% beacons')
# plt.plot(x, beacon_precent_8, 'g', marker='*', label='8% beacons')
# plt.plot(x, beacon_precent_10, 'b', marker='v', label='10% beacons')
# plt.legend()
# plt.savefig('change_beacon.pdf')
# plt.savefig('change_beacon.eps')
# plt.show()cdcdcdcdcdcd

x = [50, 100, 150, 200, 250, 300, 350, 400, 450]
dv = [8.569, 6.718, 6.502, 4.916, 3.345, 2.999, 2.156, 1.965, 1.673]
gda = [8.079, 5.974, 3.677, 3.549, 1.992, 2.018, 1.742, 1.742, 1.818]
mds_map = [10, 6.123, 4.332, 2.456, 1.637, 1.3, 1.23, 1.16, 1.027]
grolo = [8.079, 6.031, 3.607, 3.126, 1.658, 1.448, 0.665, 0.577, 0.44]
plt.figure()
plt.xlabel('Node Number')
plt.ylabel('RMSE')
plt.plot(x, dv, 'r', marker='o',ms='6', label='DV-distance')
plt.plot(x, mds_map, marker='*',ms=8, label='MDS-MAP')
plt.plot(x, gda, 'g', marker='s',ms='6', label='GDA')
plt.plot(x, grolo, 'b', marker='v',ms='6', label='GROLO-LP')
plt.legend()
plt.savefig('change_nodes_num.pdf')
plt.savefig('change_nodes_num.eps')
plt.show()