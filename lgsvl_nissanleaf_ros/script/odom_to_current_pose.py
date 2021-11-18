#!/usr/bin/env python  

import rospy
import geometry_msgs.msg as geomsg

pub_pose = None


def callback_odom(msg):
    global pub_pose

    rate=rospy.Rate(10)
    current_pose=geomsg.PoseStamped()
    current_pose.header.frame_id='odom'
    current_pose.header.stamp=rospy.Time.now()
    current_pose.pose.position = msg.pose.position
    current_pose.pose.orientation = msg.pose.orientation

    if pub_pose is not None:
        pub_pose.publish(current_pose)
        rate.sleep()


def talker():
    global pub_pose
   
    rospy.init_node('odom_to_pose', anonymous=True)
    rospy.Subscriber("/odom", geomsg.PoseStamped, callback_odom, queue_size=1)
    pub_pose = rospy.Publisher("/current_pose", geomsg.PoseStamped, queue_size=1, latch=True)
    rospy.spin()

    



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass