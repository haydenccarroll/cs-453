from action_msgs.msg import GoalStatus

from nav_msgs.msg import Odometry
from builtin_interfaces.msg import Duration # Duration {sec, nanosec}
import irobot_create_msgs
from irobot_create_msgs.msg import DockStatus
from irobot_create_msgs.msg import AudioNote # notes {int frequency, Duration max_runtime}
#from irobot_create_msgs import AudioNoteVector
from irobot_create_msgs.action import Undock, Dock, DriveDistance, DriveArc, RotateAngle, AudioNoteSequence 

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient

"""
    Defines an interface for playing sounds via the iRobot Create3 speakers
"""
class AudioManager(Node):

    def __init__(self, namespace_str='create3_05F8/'):
        super().__init__('audio_manager')
        self._audio_client = ActionClient(self, AudioNoteSequence, namespace_str + 'audio_note_sequence')


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

        rclpy.shutdown()


    def play_happy_sound(self):
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


class DockManager(Node):

    def __init__(self, dock_robot=True, namespace_str=None):
        super().__init__('driver')

        self._is_docking = dock_robot

        #topic_str
        if dock_robot:
            topic_str = 'dock'
            action_type = Dock

        else: 
            topic_str = 'undock'
            action_type = Undock

        if namespace_str is not None:
            topic_str = namespace_str + '/' + topic_str

        self._action_client = ActionClient(self, action_type, topic_str)



    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected: (')
            return

        self.get_logger().info('Goal accepted :)')

        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)


    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded! Result: is_docked = {}'.format(result.is_docked))
        else:
            self.get_logger('Goal failed with status: {0}'.format(status))

        rclpy.shutdown()


    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

        if self._is_docking:
            goal_msg = Dock.Goal()

        else:
            goal_msg = Undock.Goal()

        self.get_logger().info('Sending goal request...')
        self._send_goal_future = self._action_client.send_goal_async(
                goal_msg,
                feedback_callback=None)

        self._send_goal_future.add_done_callback(self.goal_response_callback)


class Drive(Node):

    def __init__(self):
        super().__init__('driver')
        self._action_client = ActionClient(self, DriveDistance, 'create3_05F8/drive_distance')

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

        rclpy.shutdown()


    def send_goal(self):
        self.get_logger().info('Waiting for action server...')
        self._action_client.wait_for_server()

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
        self._send_goal_future = self._action_client.send_goal_async(
                goal_msg,
                feedback_callback=self.feedback_callback)

        self._send_goal_future.add_done_callback(self.goal_response_callback)

def main(args=None):
    rclpy.init(args=args)

    dockman_node = DockManager(dock_robot=False, namespace_str='create3_05F8')
    dockman_node.send_goal()

    audio_node = AudioManager()
    audio_node.play_happy_sound()
    #rclpy.spin(audio_node)
    #action_client = DriveShape()
    #action_client.send_audio_goal()
    #rclpy.spin(action_client)


if __name__ == '__main__':
    main()
