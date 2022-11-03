import time
import rclpy
import paho.mqtt.client as mqtt

from hw1_assignment.undock import UndockNode
from hw1_assignment.dock import DockNode
from hw1_assignment.odom_sub import OdomSub

def main(args=None):
    rclpy.init(args=args)


    robotName = "create3_05F8"
    odomMsgType = None
    SubscriptionHandler(robotName, "odom", odomMsgType, publishOdom())
    # undock_node = UndockNode(robotName)
    # dock_node = DockNode(robotName)

    rclpy.shutdown()