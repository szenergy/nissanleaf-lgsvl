#!/usr/bin/env python

import rospy
import lgsvl_msgs.msg as lgsvl
import geometry_msgs.msg as geomsg
import autoware_msgs.msg as autoware

pub_twist= None

def controlcmdCallback(msg):
    global pub_twist
    twist_msg=geomsg.TwistStamped()
    twist_msg.header.stamp = rospy.Time.now()
    twist_msg.header.frame_id = "base_link"
    twist_msg.twist.linear.x=msg.cmd.linear_velocity
    twist_msg.twist.angular.z=msg.cmd.steering_angle
    if pub_twist is not None:
        pub_twist.publish(twist_msg)


def listener():
    global pub_twist
    rospy.init_node("ctrl_cmd_to_twist_raw_converter", anonymous=True)  
    rospy.Subscriber("/ctrl_cmd", autoware.ControlCommandStamped, controlcmdCallback)
    
    pub_twist = rospy.Publisher("/twist_cmd", geomsg.TwistStamped, queue_size=10)
    #pub_vehiclestatus=rospy.Publisher("/vehicle_status", autoware.VehicleStatus, queue_size=10)
    rospy.loginfo("publish twist_cmd")

    rospy.spin()

if __name__ == '__main__':
    listener()