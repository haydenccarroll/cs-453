from rclpy.action.client import ActionClient
from irobot_create_msgs.action import DockServo
from hw1_assignment.action_handler import ActionHandler

class DockNode(ActionHandler):
    def __init__(self, robotName):
        super().__init__("hw1_dock_node")
        self._client = ActionClient(self, DockServo, f'/{robotName}/dock')

    def _do(self):
        goal_msg = DockServo.Goal()
        return goal_msg