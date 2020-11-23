#!/usr/bin/env python
"""
/odom                  nav_msgs/Odometry
/current_pose          geometry_msgs/PoseStamped
"""
import rospy
import geometry_msgs.msg as geomsg
import nav_msgs.msg as navmsg

param_location = ""
gyor_x = 697237.0 
gyor_y = 5285644.0 
zala_x = 639770.0 
zala_y = 5195040.0
pub_odom = None
def odomCallBack(msg):
    global pub_odom
    pose_msg = geomsg.PoseStamped()
    pose_msg.header.stamp = rospy.Time.now()
    if param_location == "zero":
        pose_msg.pose.position.x = msg.pose.pose.position.x
        pose_msg.pose.position.y = msg.pose.pose.position.x
    elif param_location == "zala":
        pose_msg.pose.position.x = msg.pose.pose.position.x + zala_x
        pose_msg.pose.position.y = msg.pose.pose.position.x + zala_y
    else:
        pose_msg.pose.position.x = msg.pose.pose.position.x + gyor_x
        pose_msg.pose.position.y = msg.pose.pose.position.x + gyor_y
    pose_msg.pose.orientation = msg.pose.pose.orientation
    #rospy.loginfo(pose_msg)
    if pub_odom is not None:
        pub_odom.publish(pose_msg)


def listener():
    global pub_odom, param_location
    rospy.init_node("odom_to_pose_py", anonymous=True)
    rospy.loginfo("odom_to_pose_py started. Soon publishing /current_pose if /odom is ready.")
    try:
        param_location = str(rospy.get_param("lgsvl_location"))
    except:
        param_location = "gyor"
    rospy.Subscriber("/odom", navmsg.Odometry, odomCallBack)
    rospy.loginfo("lgsvl_location is " + str(param_location))
    pub_odom = rospy.Publisher("/current_pose", geomsg.PoseStamped, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    listener()
