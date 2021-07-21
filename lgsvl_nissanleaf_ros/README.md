# lgsvl Nissan Leaf ROS auxiliaries
This ROS package (`lgsvl_nissanleaf_ros`) aims to provide additional launch files and nodes to make it easier to work with lgsvl and ROS.

## Usage

In order to create `/current_pose` from `/odom` simply run:
```
rosrun lgsvl_nissanleaf_ros odom_to_pose.py
```

There are 3 default locations which can be simulated as:
```
rosparam set lgsvl_location zala
rosparam set lgsvl_location gyor
rosparam set lgsvl_location zero
rosrun lgsvl_nissanleaf_ros odom_to_pose.py
```
To start the static + dynamic trasforms and the bridge (in case of Windows), run:
```
roslaunch lgsvl_nissanleaf_ros tf_bridge.launch
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
- [lgsvl_msgs](https://github.com/lgsvl/lgsvl_msgs) LGSVL related ROS message types, clone and build in the catkin workspace
- [rosbridge-server](http://wiki.ros.org/rosbridge_server) simply install with `sudo apt install ros-$ROS_DISTRO-rosbridge-server`
- [nissan_leaf_ros](https://github.com/szenergy/nissan_leaf_ros)/nissan_brigup contains the 3D rviz model (optional for visualization in RVIZ)
- [autoware.ai](https://github.com/Autoware-AI/autoware.ai) optional if the control is done with autoware MPC realization 

## Install ROS dependencies

It is recommended to use catkin build instead of catkin_make, but it is not obilgatory. 
```
sudo apt update
sudo apt install python-catkin-tools
```

Initiialize catkin workspace if not yet done (`~/catkin_ws` is assumed).
```
mkdir ~/catkin_ws
cd ~/catkin_ws
mkdir src
catkin init
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
```

Clone the dependencies to the catkin workspace.
```
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src
cd ~/catkin_ws/src
git clone https://github.com/lgsvl/lgsvl_msgs
git clone https://github.com/ros-drivers/velodyne
git clone https://github.com/szenergy/nissan_leaf_ros
git clone https://github.com/szenergy/nissanleaf-lgsvl
git clone https://github.com/szenergy/szenergy-utility-programs
```

Build and don't forget to source bashrc.
```
catkin build lgsvl_msgs lgsvl_nissanleaf_ros velodyne gps_tf_publisher
source ~/.bashrc
```

Install rosbridge-server.
```
sudo apt install ros-$ROS_DISTRO-rosbridge-server
```

# Topics

|Topic|Type|Hz|Description|Port (sim)|Port (leaf)
|-|-|-|-|-|-|
`/velodyne_left/velodyne_points`|sensor_msgs/PointCloud2|20|Velodyne LIDAR| |
`/velodyne_right/velodyne_points`|sensor_msgs/PointCloud2|20|Velodyne LIDAR| |
`/left_os1/os1_cloud_node/points`|sensor_msgs/PointCloud2|20|Ouster LIDAR| |
`/right_os1/os1_cloud_node/points`|sensor_msgs/PointCloud2|20|Ouster LIDAR| |
`/left_os1/os1_cloud_node/imu`|sensor_msgs/Imu|100|Ouster LIDAR| |
`/right_os1/os1_cloud_node/imu`|sensor_msgs/Imu|100|Ouster LIDAR| |
`/cloud`|sensor_msgs/PointCloud2|25|SICK LIDAR| |
`/scan`|sensor_msgs/LaserScan|25|SICK LIDAR| |
`/zed_node/left/camera_info`|sensor_msgs/CameraInfo|20|ZED camera| |
`/zed_node/left/image_rect_color/compressed`|sensor_msgs/Image|20|ZED camera| |
`/vehicle_status`|autoware_msgs/VehicleStatus|100|CAN data| |
`/gps/duro/current_pose`|geometry_msgs/PoseStamped|20|Duro GPS (UTM)| |
`/gps/duro/imu`|sensor_msgs/Imu|200|Duro GPS| |
`/gps/duro/mag`|sensor_msgs/MagneticField|25|Duro GPS| |
`/gps/nova/current_pose`|geometry_msgs/PoseStamped|40|Novatel GPS (UTM)| |
`/gps/nova/imu`|sensor_msgs/Imu|200|Novatel GPS| |
`/current_pose`|geometry_msgs/PoseStamped|20|Current pose from the used GPS| |
`/tf`|tf2_msgs/TFMessage|500+|Transform| |

Some important types:

- [`geometry_msgs/PoseStamped`](http://docs.ros.org/en/melodic/api/geometry_msgs/html/msg/PoseStamped.html)
- [`sensor_msgs/PointCloud2`](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/PointCloud2.html)
- [`sensor_msgs/LaserScan`](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/LaserScan.html)
- [`sensor_msgs/NavSatFix`](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/NavSatFix.html) 
- [`sensor_msgs/Imu`](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/Imu.html)
- [`sensor_msgs/MagneticField`](http://docs.ros.org/en/melodic/api/sensor_msgs/html/msg/MagneticField.html) 

# Notes

Install `v0.1-beta` on windows:
<p align="center">
    <a href="https://www.youtube.com/watch?v=EH_U3JtfVO4"><img src="../Figures/NissanLeafLGSVLvideo01.png" width=400 /></a>
</p>