from rclpy.action.client import ActionClient
from irobot_create_msgs.action import DriveDistance
from hw1_assignment.action_handler import ActionHandler

class ForwardNode(ActionHandler):
    def __init__(self, robotName):
        super().__init__("hw1_forward_node")
        self._client = ActionClient(self, DriveDistance, f'/{robotName}/drive_distance')

    def _do(self, distance, speed):
        goal_msg = DriveDistance.Goal()
        goal_msg.distance = float(distance)
        goal_msg.max_translation_speed = float(speed)

        return goal_msg
