from action_msgs.msg import GoalStatus
from builtin_interfaces.msg import Duration # Duration {sec, nanosec}

# iRobot Types
# msg types
from irobot_create_msgs.msg import Dock, AudioNote # notes {int frequency, Duration max_runtime}
# action types
from irobot_create_msgs.action import AudioNoteSequence

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile



"""
    Defines an interface for playing sounds via the iRobot Create3 speakers
"""
class AudioManager(Node):

    def __init__(self, namespace_str=None):
        super().__init__('audio_manager')

        topic_str = 'audio_note_sequence'
        if namespace_str is not None:
            topic_str = namespace_str + '/' + topic_str

        self._audio_client = ActionClient(self, AudioNoteSequence, topic_str)


    def get_logger(self):
        return self._logger


    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected: (')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)


    def feedback_callback(self, feedback):
        self.get_logger().info('Received feedback: \n\titerations_played = {0}, \n\tcurrent_runtime [{1}s, {2}ns]'.format(feedback.iterations_played, 
            feedback.current_runtime.sec, 
            feedback.current_runtime.nanosec))


    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded! Result: complete = {0}, iterations = {1}, seconds = {2}, nanoseconds = {3}'.format(result.complete, result.iterations_played, result.runtime.sec, result.runtime.nanosec))
        else:
            self.get_logger('Goal failed with status: {0}'.format(status))

        self.destroy_node()


    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._audio_client.wait_for_server()

        goal_msg = AudioNoteSequence.Goal()
        #print('iterations type: ', type(goal_msg.iterations))
        #print('note sequence: ', type(goal_msg.note_sequence))
        #print(dir(irobot_create_msgs.msg._audio_note_vector.AudioNoteVector.notes))
        goal_msg.iterations = 1
        goal_msg.note_sequence.notes = [
                AudioNote(frequency=392, max_runtime=Duration(sec=0, nanosec=177500000)),
                AudioNote(frequency=523, max_runtime=Duration(sec=0, nanosec=355000000)),
                AudioNote(frequency=587, max_runtime=Duration(sec=0, nanosec=177500000)),
                AudioNote(frequency=784, max_runtime=Duration(sec=0, nanosec=533000000)),
                ]

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._audio_client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

        return self._send_goal_future