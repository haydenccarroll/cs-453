import rclpy
from paho.mqtt import client as mqtt
from irobot_create_msgs.msg import 
class OdomSub(rclpy.node.Node):
    def __init__(self, robotName, mqttIP):
        super().__init__(robotName + " odom subscription node")
        self.mqtt_client = mqtt.Client("odom pub client")
        self.mqtt_client.connect(mqttIP)

        self.sub_client = self.create_subscription(
            self,
            String,
            robotName + "/odom",
            self._result_callback)

    def _result_callback(self, future):
        goal_handle = future.result()
        goal_handle.
        result = client.publish("gcs/robot/odom", msg)
        pass
