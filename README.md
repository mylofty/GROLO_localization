#Description
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

use data "./data/nodes_100_beacon_5", you can get the picture:

![image](https://github.com/mylofty/GROLO_localization/raw/master/data/nodes_100_beacon_5/img/result_random_dvdistance.jpg)

![image](https://github.com/AITTSMD/MTCNN-Tensorflow/raw/master/test/lala/img_414.jpg)

![哆啦A梦](https://cdoco.com/images/duolaameng.jpeg "哆啦A梦")

![random](data/nodes_100_beacon_5/result_random_dvdistance.jpg, "ddd")
![random](data/nodes_100_beacon_5/result_random_dvdistance.jpg)

