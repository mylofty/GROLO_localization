import matplotlib.pyplot as plt
END = 7
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
dv = [4.85, 4.52, 4.18, 2.1, 1.95, 1.94, 1.90, 3.4, 4.3, 3.69]
gda = [3.44, 2.94, 2.67, 1.76, 1.72, 1.70, 1.68, 1.628, 1.477, 1.47]
mds_map = [1.659, 1.194, 1.142, 1.16, 1.16, 1.16, 1.11, 1.09, 1.03, 1.03]
grolo = [3.137, 2.78, 2.30, 0.55, 0.54, 0.53, 0.51, 0.5, 0.45, 0.5]
plt.figure()
plt.xlabel('Beacon Ratio(%)')
plt.ylabel('RMSE')
plt.plot(x[0:END], dv[0:END], marker='o',ms='8', label='DV-distance')
plt.plot(x[0:END], mds_map[0:END], marker='*',ms='10', label='MDS-MAP')
plt.plot(x[0:END], gda[0:END], marker='s',ms='7', label='GDA')
plt.plot(x[0:END], grolo[0:END], marker='v',ms='8', label='GROLO-LP')
plt.legend()
plt.savefig('diff_beacon.pdf')
plt.savefig('diff_beacon.eps')
plt.show()