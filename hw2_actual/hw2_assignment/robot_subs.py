from paho.mqtt import client as mqtt
from geometry_msgs.msg import Pose


class Robot:
    def __init__(self, id):
        self.id = id
        self.pose = None

class RobotSubs:
    def __init__(self, robot_ids, mqtt_client):
        self.mqtt_client = mqtt_client
        self.robot_ids = robot_ids
        self.robot_list = [Robot(id) for id in self.robot_ids]

        for robot_id in self.robot_ids:
            self.mqtt_client.subscribe(
                    f"irobot_create3_swarm/gcs_pose/{robot_id}"
                )
        self.mqtt_client.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        print("ON MESSAGE: ", msg)
        for robot in self.robot_list:
            if robot.id in msg.topic:
                robot.pose = msg.payload
                return

    def get_robots(self):
        return self.robot_list

    def get_robot(self, id):
        for robot in self.robot_list:
            if robot.id == id:
                return robot
        return None

