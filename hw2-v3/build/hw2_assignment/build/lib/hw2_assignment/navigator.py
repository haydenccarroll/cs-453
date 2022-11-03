# ros2 types
from std_msgs.msg import String
from action_msgs.msg import GoalStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Quaternion, Point
from builtin_interfaces.msg import Duration # Duration {sec, nanosec}

# iRobot Types
# msg types
from irobot_create_msgs.msg import Dock, AudioNote # notes {int frequency, Duration max_runtime}
# action types
from irobot_create_msgs.action import Undock, DockServo, DriveDistance, DriveArc, RotateAngle, AudioNoteSequence, NavigateToPosition

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import Executor, SingleThreadedExecutor, MultiThreadedExecutor
from rclpy.qos import QoSProfile




class Navigate(Node):

    def __init__(self, pose=None, achieve_orientation=True, namespace_str=None):
        super().__init__('navigator')

        self._target_pose = pose
        self._achieve_orientation = achieve_orientation

        topic_str = 'navigate_to_position'
        if namespace_str is not None:
            topic_str = namespace_str + '/' + topic_str
            self.get_logger().info('action used = {}'.format(topic_str))

        self._action_client = ActionClient(self, NavigateToPosition, topic_str)


    def feedback_callback(self, feedback):
    	feedback = feedbakck.feedback
    	self.get_logger().info('Feedback: \n\tnavigate_state = {},\n\tremaining_travel_angle = {},\n\tremaining_travel_distance = {}'.format(
            feedback.navigate_state,
            feedback.remaining_travel_angle,
            feedback.remaining_travel_distance))


    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        else:
            self.get_logger('Goal failed with status: {0}'.format(status))

        self.destroy_node()


    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)



    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = NavigateToPosition.Goal()
        goal_msg.goal_pose.pose = self._target_pose
        goal_msg.achieve_goal_heading = self._achieve_orientation

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(
                    goal_msg, 
                    feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)