from rclpy.action.client import ActionClient
from irobot_create_msgs.action import NavigateToPosition
from action_handler import ActionHandler

class GoalDriver(ActionHandler):
    # datatype of goal_pose is geometry_msgs/PoseStamped
    def __init__(self, robotName, goal_pose):
        super().__init__(f"{robotName}_goal_driver_node")
        self.goal_pose = goal_pose
        self._client = ActionClient(self, NavigateToPosition, f'/{robotName}/navigate_to_position')

    def _start(self):
        goal_msg = NavigateToPosition.Goal()
        goal_msg.goal_pose = self.goal_pose
        return goal_msg
