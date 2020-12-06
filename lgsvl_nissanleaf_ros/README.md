# lgsvl Nissan Leaf ROS auxiliaries
This ROS package (`lgsvl_nissanleaf_ros`) aims to provide additional launch files and nodes to make it easier to work with lgsvl and ROS.

## Usage

In order to create `/current_pose` from `/odom` simply run:
```
rosrun lgsvl_nissanleaf_ros odom_to_pose.py
```

There are 3 default locations whic can be simulated as:
```
rosparam set lgsvl_location zala
rosparam set lgsvl_location gyor
rosparam set lgsvl_location zero
rosrun lgsvl_nissanleaf_ros odom_to_pose.py
```

To start the static + dynamic trasforms, the vehicle model and the bridge (in case of Windows), run:
```
roslaunch lgsvl_nissanleaf_ros tf_model_bridge.launch
```

To start the static + dynamic trasforms, and the 3D vehicle model:
```
roslaunch lgsvl_nissanleaf_ros tf_model.launch
```

## Dependencies
- [nissan_leaf_ros](https://github.com/szenergy/nissan_leaf_ros)/nissan_brigup contains the 3D rviz model