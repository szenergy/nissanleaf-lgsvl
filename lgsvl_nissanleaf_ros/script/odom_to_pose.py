#!/usr/bin/env python
"""
/odom                  nav_msgs/Odometry
/current_pose          geometry_msgs/PoseStamped
"""
import rospy
import geometry_msgs.msg as geomsg
import nav_msgs.msg as navmsg
import std_msgs.msg as stdmsg

param_location = ""
gyor_x = 697237.0 
gyor_y = 5285644.0 
zala_x = 639770.0 
zala_y = 5195040.0
pub_nova_odom = None
pub_duro_odom = None

def odomNovaCallBack(msg):
    global pub_nova_odom
    pose_msg = geomsg.PoseStamped()
    pose_msg.header.stamp = rospy.Time.now()
    pose_msg.header.frame_id = "map"
    if param_location == "zero":
        pose_msg.pose.position.x = msg.pose.pose.position.x
        pose_msg.pose.position.y = msg.pose.pose.position.y
    elif param_location == "zala":
        pose_msg.pose.position.x = msg.pose.pose.position.x + zala_x
        pose_msg.pose.position.y = msg.pose.pose.position.y + zala_y
    else:
        pose_msg.pose.position.x = msg.pose.pose.position.x + gyor_x
        pose_msg.pose.position.y = msg.pose.pose.position.y + gyor_y
    pose_msg.pose.orientation = msg.pose.pose.orientation
    #rospy.loginfo(pose_msg)
    if pub_nova_odom is not None:
        pub_nova_odom.publish(pose_msg)

def odomDuroCallBack(msg):
    global pub_duro_odom, pub_duro_string
    pose_msg = geomsg.PoseStamped()
    pose_msg.header.stamp = rospy.Time.now()
    pose_msg.header.frame_id = "map"
    if param_location == "zero":
        pose_msg.pose.position.x = msg.pose.pose.position.x
        pose_msg.pose.position.y = msg.pose.pose.position.y
    elif param_location == "zala":
        pose_msg.pose.position.x = msg.pose.pose.position.x + zala_x
        pose_msg.pose.position.y = msg.pose.pose.position.y + zala_y
    else:
        pose_msg.pose.position.x = msg.pose.pose.position.x + gyor_x
        pose_msg.pose.position.y = msg.pose.pose.position.y + gyor_y
    pose_msg.pose.orientation = msg.pose.pose.orientation
    #rospy.loginfo(pose_msg)
    if pub_duro_odom is not None:
        pub_duro_odom.publish(pose_msg)
        stri = stdmsg.String()
        stri.data = "Simulated RTK"
        pub_duro_string.publish(stri)



def listener():
    global pub_nova_odom, pub_duro_odom, param_location, pub_duro_string
    rospy.init_node("odom_to_pose_py", anonymous=True)
    rospy.loginfo("odom_to_pose_py started. Soon publishing /gps/nova/current_pose and /gps/duro/current_pose if /gps/nova/odom and /gps/duro/odom is ready.")
    try:
        param_location = str(rospy.get_param("lgsvl_location"))
    except:
        param_location = "gyor"
    rospy.Subscriber("/gps/nova/odom", navmsg.Odometry, odomNovaCallBack)
    rospy.Subscriber("/gps/duro/odom", navmsg.Odometry, odomDuroCallBack)
    rospy.loginfo("lgsvl_location is " + str(param_location))
    pub_nova_odom = rospy.Publisher("/gps/nova/current_pose", geomsg.PoseStamped, queue_size=10)
    pub_duro_odom = rospy.Publisher("/gps/duro/current_pose", geomsg.PoseStamped, queue_size=10)
    pub_duro_string = rospy.Publisher("/gps/duro/status_string", stdmsg.String, queue_size=10)
    rospy.spin()

if __name__ == '__main__':
    listener()
