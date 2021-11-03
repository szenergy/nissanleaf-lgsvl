#!/usr/bin/env python  

"""
Publishes a ROS marker to visualize the current steering with a marker in RVIZ
"""
import numpy as np
import rospy
import autoware_msgs.msg as autmsg
import geometry_msgs.msg as geomsg
import std_msgs.msg as stdmsg
from scipy.spatial.transform import Rotation as R
import tf2_ros
import math
#import matplotlib.pyplot as plt

speed_mps = 0.0
t1=0.0
x=y=0.0
pos_x = pos_y = theta = 0.0 
r=0.0


def vehicle_status_callback(data):
    global t1,pos_x,pos_y,x,y,theta,speed_mps,r
   
    previous_speed=speed_mps
    wheel_ang_rad=data.angle
    speed_mps=data.speed
    length = 2.7 # the disatance between the rear and the front axle TODO from param
    mod_theta=theta
    if mod_theta > math.pi:
        mod_theta = theta - (2*math.pi)
    elif mod_theta < - math.pi:
        mod_theta = theta + (2*math.pi)


    if speed_mps > 20:
        speed_mps = previous_speed


    vx = speed_mps*np.cos(wheel_ang_rad)
    
    previous_t=t1
    t1=rospy.Time.now().to_sec() 
    delta=t1-previous_t

    if delta > 1:
      delta=0.01
    
    theta += delta * vx / length * np.tan(wheel_ang_rad) 

    r=R.from_euler('z',mod_theta, degrees=False)
    


    pos_x = delta * vx * np.cos(mod_theta)
    pos_y = delta * vx * np.sin(mod_theta)

    # pos_x = delta * speed_mps * np.cos(mod_theta)
    # pos_y = delta * speed_mps * np.sin(mod_theta)
        
    x=x+pos_x
    y=y+pos_y
    

    pose=geomsg.PoseStamped()
    pose.header.stamp = rospy.Time.now()
    pose.header.frame_id="odom"
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.position.z = 0.0
    pose.pose.orientation.x = r.as_quat()[0]
    pose.pose.orientation.y = r.as_quat()[1]
    pose.pose.orientation.z = r.as_quat()[2]
    pose.pose.orientation.w = r.as_quat()[3]

    br = tf2_ros.TransformBroadcaster()
    t = geomsg.TransformStamped()
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "odom"
    t.child_frame_id = "base_link"
    t.transform.translation.x = x
    t.transform.translation.y = y
    t.transform.translation.z = 0.0
    
    t.transform.rotation.x = r.as_quat()[0]
    t.transform.rotation.y = r.as_quat()[1]
    t.transform.rotation.z = r.as_quat()[2]
    t.transform.rotation.w = r.as_quat()[3]

    br.sendTransform(t)

    th = stdmsg.Float32()
    th.data = theta
    pub_theta.publish(th)
    pub_pose.publish(pose)



if __name__ == '__main__':
    global pub_pose

    rospy.init_node('odometry')
    rospy.Subscriber('/vehicle_status', autmsg.VehicleStatus,  vehicle_status_callback)
    pub_pose = rospy.Publisher("/odom", geomsg.PoseStamped, queue_size=1, latch=True)
    pub_theta = rospy.Publisher("/theta", stdmsg.Float32, queue_size=1, latch=True)
    rospy.loginfo("odom started")
    rospy.spin()