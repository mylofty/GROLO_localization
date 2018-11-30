
import matplotlib.pyplot as plt

x = [50, 100, 150, 200, 250, 300, 350, 400]
beacon_precent_5 = [8.514, 6.624, 4.47, 3.61, 2.11, 1.5, 1.02, 0.8]
beacon_precent_8 = [8.427, 6.164, 3.4936, 2.268, 1.90, 1.24, 0.75, 0.5]
beacon_precent_10 = [7.85, 5.901, 2.858, 2.00, 1.62, 0.95, 0.55, 0.4]

plt.figure()
plt.xlabel('node number')
plt.ylabel('RMSE')
plt.plot(x, beacon_precent_5, 'r', marker='o', label='5% beacons')
plt.plot(x, beacon_precent_8, 'g', marker='*', label='8% beacons')
plt.plot(x, beacon_precent_10, 'b', marker='v', label='10% beacons')
plt.legend()
plt.savefig('change_beacon.pdf')
plt.savefig('change_beacon.eps')
plt.show()