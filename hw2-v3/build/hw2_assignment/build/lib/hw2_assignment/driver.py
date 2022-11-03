#ros2 types
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



class Drive(Node):

    def __init__(self, namespace_str=None):
        super().__init__('driver')

        topic_str = 'drive_distance'
        if namespace_str is not None:
            topic_str = namespace_str + '/' + topic_str

        self._action_client = ActionClient(self, DriveDistance, topic_str)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)


    def feedback_callback(self, feedback):
    	feedback = feedback.feedback
    	self.get_logger().info('Received feedback: \n\tremaining_travel_distance = {}'.format(feedback.remaining_travel_distance))

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        else:
            self.get_logger('Goal failed with status: {0}'.format(status))

        # execute callbacks, and clear
        for callback in self._action_complete_callbacks:
            self.get_logger().info('calling complete callback')
            callback(future)

        self._action_complete_callbacks = []


    def send_goal(self, distance=0.0, velocity=0.3, goal_completed_callbacks=[]):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = DriveDistance.Goal()
        goal_msg.distance = distance
        goal_msg.max_translation_speed = velocity

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)
        self._action_complete_callbacks = goal_completed_callbacks

        return self._send_goal_future