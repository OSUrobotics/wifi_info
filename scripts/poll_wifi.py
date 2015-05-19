#!/usr/bin/env python

import rospy
from pythonwifi.iwlibs import Wireless
from wifi_info.msg import WifiInfo


def main():
    rospy.init_node('wifi_poller')
    poll_freq = rospy.get_param('~poll_freq', 1)
    interface = rospy.get_param('~interface', 'eth1')
    frame_id = rospy.get_param('~frame_id', 'base_link')

    pub = rospy.Publisher('wifi_info', WifiInfo)

    wifi = Wireless(interface)
    poll_rate = rospy.Rate(poll_freq)
    while not rospy.is_shutdown():
        info = WifiInfo()
        info.header.stamp = rospy.Time.now()
        info.header.frame_id = frame_id

        try:
            info.essid = wifi.getEssid()
            info.interface = interface
            info.status = WifiInfo.STATUS_DISCONNECTED
            if info.essid:
                info.frequency = float(wifi.getFrequency().split(' ')[0])
                info.APaddr = wifi.getAPaddr()
                info.status = WifiInfo.STATUS_CONNECTED
        except IOError:
            # This can happen with an invalid iface
            info.status = WifiInfo.STATUS_ERROR
        except Exception, e:
            info.status = WifiInfo.STATUS_ERROR
            rospy.logerr('Error: %s' % e)

        pub.publish(info)
        poll_rate.sleep()

if __name__ == '__main__':
    main()
