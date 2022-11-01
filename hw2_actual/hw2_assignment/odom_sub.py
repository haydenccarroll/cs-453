from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from paho.mqtt import client as mqtt
from nav_msgs.msg import Odometry

class OdomSub(Node):
    def __init__(self, robot_name, mqtt_client):
        super().__init__(f"{robot_name}_odom_sub_node")
        self.mqtt_client = mqtt_client
        self.robot_id = robot_name

        # QoS profile:
        #   Reliability: BEST_EFFORT
        #   History (Depth): KEEP_LAST (5)
        #   Durability: VOLATILE
        #   Lifespan: Infinite
        #   Deadline: Infinite
        #   Liveliness: AUTOMATIC
        #   Liveliness lease duration: Infinite
        self.qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=5
        )

        self.sub_client = self.create_subscription(
            Odometry,
            "/" + robot_name + "/odom",
            self._result_callback,
            self.qos)

    def _result_callback(self, future):
        pose = future.pose
        twist = future.twist

        msg = dict()
        msg["pose"] = pose
        msg["twist"] = twist
        result = self.mqtt_client.publish(
            f"irobot_create3_swarm/gcs_pose/{self.robot_id}",
            str(msg))
