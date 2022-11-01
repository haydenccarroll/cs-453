import rclpy
from rclpy.action.client import ActionClient
from irobot_create_msgs.action import Undock
from hw1_assignment.action_handler import ActionHandler

class UndockNode(ActionHandler):
    def __init__(self, robotName):
        super().__init__("hw1_undock_node")
        self._client = ActionClient(self, Undock, f'/{robotName}/undock')

    def _do(self):
        goal_msg = Undock.Goal()
        return goal_msg
