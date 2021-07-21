#!/usr/bin/env python

import rospy
import lgsvl_msgs.msg as lgsvl
import geometry_msgs.msg as geomsg
autoware_installed = True
try:
    import autoware_msgs.msg as autoware
except:
    autoware_installed = False


pub_velocity = None
pub_vehiclestatus= None


def canCallBack(msg):
    global pub_velocity,pub_vehiclestatus, autoware_installed

    #publish current_velocity
    vel_msg=geomsg.TwistStamped()
    vel_msg.header.stamp = rospy.Time.now()
    vel_msg.header.frame_id = "base_link"
    vel_msg.twist.linear.x=msg.speed_mps                #m/s
    vel_msg.twist.angular.z=-msg.steer_pct*31*(3.14/180)  #rad  todo:revision stearing limit
    if pub_velocity is not None:
        pub_velocity.publish(vel_msg)

    # publish vehicle_status    
    vehicle_msg=autoware.VehicleStatus()
    vehicle_msg.header.stamp = rospy.Time.now()
    vehicle_msg.header.frame_id = "base_link"
    vehicle_msg.speed=msg.speed_mps                 #m/s
    vehicle_msg.angle=-msg.steer_pct*39.4*(3.14/180)     #rad        todo:revision steering limit
    if pub_vehiclestatus is not None:
        pub_vehiclestatus.publish(vehicle_msg)


def listener():
    global pub_velocity,pub_vehiclestatus
    rospy.init_node("can_bus_to_autoware", anonymous=True)  
    rospy.Subscriber("/canbus", lgsvl.CanBusData, canCallBack)
    
    pub_velocity = rospy.Publisher("/current_velocity", geomsg.TwistStamped, queue_size=10)
    if autoware_installed is True:
        pub_vehiclestatus=rospy.Publisher("/vehicle_status", autoware.VehicleStatus, queue_size=10)
    else:
        rospy.logwarn("Autoware is not installed")
    rospy.loginfo("current_velocity and vehicle_status are publishing")

    rospy.spin()

if __name__ == '__main__':
    listener()