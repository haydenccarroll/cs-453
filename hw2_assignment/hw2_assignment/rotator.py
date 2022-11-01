# ros2 types
from std_msgs.msg import String
from action_msgs.msg import GoalStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Quaternion, Point
from builtin_interfaces.msg import Duration # Duration {sec, nanosec}

# iRobot Types
# action types
from irobot_create_msgs.action import RotateAngle

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile


class Rotate(Node):

    def __init__(self,  namespace_str=None):
        super().__init__('rotator')

        topic_str = 'rotate_angle'
        if namespace_str is not None:
            topic_str = namespace_str + '/' + topic_str

        self.get_logger().info(f'creating action server for {topic_str}')

        self._action_client = ActionClient(self, RotateAngle, topic_str)

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
    	self.get_logger().info('Received feedback: \n\tremaining_angle_travel = {}'.format(feedback.remaining_angle_travel))

    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded!')
        else:
            self.get_logger('Goal failed with status: {0}'.format(status))

        # call callbacks and clear list
        for callback in self._action_complete_callbacks:
            self.get_logger().info('calling complete callback')
            callback(future)

        self._action_complete_callbacks = []


    def send_goal(self, degrees=0.0, angular_velocity=1.9, goal_completed_callbacks=[]):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        goal_msg = RotateAngle.Goal()
        goal_msg.angle = (degrees / 180) * 3.14
        goal_msg.max_rotation_speed = angular_velocity

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)
        self._action_complete_callbacks = goal_completed_callbacks

        return self._send_goal_future