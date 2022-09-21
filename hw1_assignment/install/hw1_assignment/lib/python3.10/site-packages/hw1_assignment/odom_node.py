import rclpy
from nav_msgs.msg import Odometry

class OdomNode(rclpy.node.Node):
    def __init__(self, robotName):
        super().__init__("hw1_odom_node")
        self.get_logger().info("HW1 program odom node has been created.")
        self.odomQos = rclpy.qos.QoSProfile(reliability=2, history=1, depth=5, durability=2)
        self.odomSub = self.create_subscription(Odometry, f"/{robotName}/odom", self.set_position_from_odom, self.odomQos)
        self.pose = Odometry().pose.pose

    def set_position_from_odom(self, msg):
        print("ODOM STUFF")
        self.pose = msg.pose.pose
