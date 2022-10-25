from irobot_create_msgs.action import Undock
from irobot_create_msgs.msg import DockStatus

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import rclpy.qos as QoS 

class MinimalClient(Node):

    def __init__(self):
        super().__init__('minimalclient')

    def feedback_callback(self, feedback):
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback.sequence))

    def dock_msg_cb(self, feedback):
        self.get_logger().info('Received feedback: {0}'.format(feedback.feedback.sequence))
        


def main():
    print('starting node')
    rclpy.init()
    node = rclpy.create_node('minimal_subscriber')

    subscription = node.create_subscription(
        DockStatus, 'create3_05F8/dock', lambda msg: node.get_logger().info('I heard: "%s"' % msg.data), QoS.qos_profile_sensor_data)
    subscription  # prevent unused variable warning
    
    rclpy.spin(node)
    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
