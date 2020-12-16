#!/usr/bin/env python

import rospy, rostopic, roslaunch, rospkg, tf
import os.path


rospack=rospkg.RosPack()
localizer=rospy.get_param('/gps_localizer')

rospy.init_node('gps_localizer', anonymous=True)

if localizer is not None and localizer=='duro':


    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launchst_tf_duro = os.path.join(rospack.get_path("nissan_bringup"), "launch/tf_setup/tf_duro_global_frame_tf_publisher.statictf.launch")
    launch = roslaunch.parent.ROSLaunchParent(uuid, [launchst_tf_duro])
    launch.start()
    rospy.loginfo("gps_static Duro started")


elif localizer is not None and localizer=='nova':
    uuid = roslaunch.rlutil.get_or_generate_uuid(None, False)
    roslaunch.configure_logging(uuid)
    launchst_tf_nova = os.path.join(rospack.get_path("nissan_bringup"), "launch/tf_setup/tf_novatel_global_frame_tf_publisher.statictf.launch")
    launch = roslaunch.parent.ROSLaunchParent(uuid, [launchst_tf_nova])
    launch.start()
    rospy.loginfo("gps_static Nova started")
else:
    rospy.loginfo("no localizer param set")


rospy.spin()