import rclpy
from rclpy.action.client import ActionClient
from irobot_create_msgs.action import Undock
from geometry_msgs.msg import Twist

class DriveNode(rclpy.node.Node):
    def __init__(self, robotName):
        super().__init__("hw1_drive_node")
        self.get_logger().info("HW1 program driver node has been created.")
        self.undock_client = ActionClient(self, Undock, f'/{robotName}/undock')
        self.drivePub = self.create_publisher(Twist, f"/{robotName}/cmd_vel", 10)

    def undock(self):
        goal_msg = Undock.Goal()
        self.undock_client.wait_for_server()
        return self.undock_client.send_goal_async(goal_msg)

    def drive_forward(self):
        msg = Twist()
        msg.linear.x = 1.0
        self.drivePub.publish(msg)

    def figure4(self):
        pass

    def spinaround(self):
        pass

    def movetodock(self):
        pass

    def dock(self):
        pass
