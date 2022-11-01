# ros2 types
from std_msgs.msg import String
from action_msgs.msg import GoalStatus
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Quaternion, Point
from builtin_interfaces.msg import Duration # Duration {sec, nanosec}

# iRobot Types
# msg types
from irobot_create_msgs.msg import Dock # notes {int frequency, Duration max_runtime}
# action types
from irobot_create_msgs.action import Undock, DockServo

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile

class DockManager(Node):

    def __init__(self, lock_node=True, dock_robot=None, namespace_str=None, dock_callback=None, undock_callback=None):
        super().__init__('dock_manager')

        self._is_docking = dock_robot
        self._dock_status_known = False
        self._docking_operation_running = False
        self._lock_node = lock_node # if set, don't allow any actions to run from this node
        self._robot_docked_callback = dock_callback
        self._robot_undocked_callback = undock_callback

        # calculate topic for dock status topic
        dock_topic = 'dock' 
        if namespace_str is not None:
            dock_topic = namespace_str + '/' + dock_topic

        dock_qos = QoSProfile(
                reliability=rclpy.qos.ReliabilityPolicy.BEST_EFFORT,
                depth=5,
                durability=rclpy.qos.DurabilityPolicy.VOLATILE,
            )

        self._dock_status_sub = self.create_subscription(Dock, dock_topic, self.dock_status_callback, dock_qos)


        # create action clients
        dock_topic_str = 'dock'
        undock_topic_str = 'undock'

        if namespace_str is not None:
            dock_topic_str = namespace_str + '/' + dock_topic_str
            undock_topic_str = namespace_str + '/' + undock_topic_str
            self.get_logger().info('action clients with namespace created : {} and {}'.format(dock_topic_str, undock_topic_str))

        self._dock_action_client = ActionClient(self, DockServo, dock_topic_str)
        self._undock_action_client = ActionClient(self, Undock, undock_topic_str)


    # set dock status flags
    def dock_status_callback(self, msg):
        #self.get_logger().info('dock_visible = {}, is_docked = {}'.format(msg.dock_visible, msg.is_docked))
        self._dock_status_known = True

        current_state = msg.is_docked

        # if robot changed state and we have a callback, call it
        if self._is_docked is not None:
            previous_state = self._is_docked      

            # robot dock state changed?
            if previous_state is not current_state:
                switcher = {
                    True: self._robot_docked_callback,
                    False: self._robot_undocked_callback
                } 

                ref = switcher.get(current_state, 'invalid')
                if ref is not None:
                    ref()

        self._is_docked = msg.is_docked
        self._dock_visible = msg.dock_visible

        if not self._docking_operation_running:
            self.send_goal()



    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected: (')
            # clear callbacks for action completion
            self._action_complete_callbacks = []
            return

        self.get_logger().info('Goal accepted :)')
        #self._dock_status_sub.destroy() # stop this callback from being called again

        self._get_result_future = goal_handle.get_result_async()

        # add callbacks passed to this object in send_goal()
        for cb in self._action_complete_callbacks:
            self._get_result_future.add_done_callback(cb)

        self._get_result_future.add_done_callback(self.get_result_callback)


    def get_result_callback(self, future):
        result = future.result().result
        status = future.result().status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info('Goal succeeded! Result: is_docked = {}'.format(result.is_docked))
        else:
            self.get_logger().error('Goal failed with status: {0}'.format(status))

        # clear semaphore preventing new actions
        self._docking_operation_running = False

        self._action_complete_callbacks = []
        #self.destroy_node()


    def force_send_goal(self, goal_completed_callbacks=[], assert_docked=False):
        self._lock_node = False
        self.send_goal(goal_complete_callbacks=goal_completed_callbacks, assert_dock_status=assert_docked)
        self._lock_node = True


    def send_goal(self, goal_complete_callbacks=[], assert_dock_status=None):
        # check if this node is allowed to start an action
        if self._lock_node:
            #self.get_logger().warning('node locked')
            return

        self.get_logger().info('Waiting for action server...')

        # set dock status and execute action, regardless of true status
        # use when don't want this to depend on dock status msg
        if assert_dock_status is not None:
            self._dock_status_known = True
            self._is_docked = assert_dock_status

        action_client = None
        goal_msg = None

        if self._dock_status_known:
            if self._is_docked: # undock the robot
                self.get_logger().info('Undocking robot...')
                action_client = self._undock_action_client
                goal_msg = Undock.Goal()
                 
            elif self._dock_visible: # dock the robot
                self.get_logger().info('Docking robot...')
                action_client = self._dock_action_client
                goal_msg = DockServo.Goal()

            else:
                self.get_logger().error('not enough known to proceed with docking, returning until next attempt')
                self._docking_operation_running = False
                return

        else:
            self.get_logger().warning('Dock status not known yet... wait a bit and retry')
            self._docking_operation_running = False
            return None

        self.get_logger().info('Sending goal request...')
        self._docking_operation_running = True
        # save the callbacks to be called when this action completes
        self._action_complete_callbacks = goal_complete_callbacks

        self._send_goal_future = action_client.send_goal_async(goal_msg, feedback_callback=None)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

        return self._send_goal_future