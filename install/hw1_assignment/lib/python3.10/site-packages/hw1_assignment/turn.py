import math

from rclpy.action.client import ActionClient
from irobot_create_msgs.action import DriveArc
from hw1_assignment.action_handler import ActionHandler

class TurnNode(ActionHandler):
    def __init__(self, robotName):
        super().__init__("hw1_turn_node")
        self._client = ActionClient(self, DriveArc, f'/{robotName}/drive_arc')

    def _do(self, deg, speed):
        goal_msg = DriveArc.Goal()
        goal_msg.angle = float(deg) * math.pi / 180
        goal_msg.max_translation_speed = float(speed)

        return goal_msg
