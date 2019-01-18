# Description
this is the part of localization in paper: GROLO: Realistic Range-based Localization for Mobile IoTs through Global Rigidity 	<br>
In this repository, we mainly to estimate the position of robots through GROLO algorithm.
# Dependencies
tensorflow	<br/>
python

# Some Details
In this repository, you can choose two kinds of method to solve the problem. In  triangle extension stage, you  can use single pair of parents or more pair of parents, and you will get two different solution.		<br/>

1. Firstly, you need to configure the code in config.py, you have to choose your origin data in folder "./data/" 
,which create by "./data/crerate_nodes.py".

2. you need to execute ./main.py to run single pair of parents' method, or run ./main_more_parents.py to run more pair of parents' method

3. you can execute ./vasualzation.py to see the picture by three method.

# Result

1. use data "./data/nodes_100_beacon_5", you can get the picture:	<br>
this is 5 beacon, 100 nodes in 100 * 100 size of space,  use dv-distance , Stochastic gradient descent, GROLO, in this algorithm, we use single pair of parents

	![image](https://github.com/mylofty/GROLO_localization/raw/master/data/nodes_100_beacon_5/img/result_random_dvdistance.jpg)
	![image](https://github.com/mylofty/GROLO_localization/raw/master/data/nodes_100_beacon_5/img/result_random_gradient.jpg)
	![image](https://github.com/mylofty/GROLO_localization/raw/master/data/nodes_100_beacon_5/img/result_random_GROLO.jpg)

2. when use more pair of parents, you can see "./data/nodes_50_beacon_5_28_more_parents"	<br/>
this is 5 beacon, 50 nodes in 100 * 100 size of space, communicate distance is 28,  use dv-distance , Stochastic gradient descent, GROLO, in this algorithm, we use more pair of parents

	![image](https://github.com/mylofty/GROLO_localization/raw/master/data/nodes_50_beacon_5_28_more_parents/img/result_random_dvdistance.jpg)

	![image](https://github.com/mylofty/GROLO_localization/raw/master/data/nodes_50_beacon_5_28_more_parents/img/result_random_gradient.jpg)

	![image](https://github.com/mylofty/GROLO_localization/raw/master/data/nodes_50_beacon_5_28_more_parents/img/result_random_GROLO.jpg)

3. we find  the communication range setting to  ![](https://latex.codecogs.com/gif.latex?2.5\times\sqrt{(S/n)}) is better, and the selection of beacon is important, but it is easy for mobile device.
END!
END!



