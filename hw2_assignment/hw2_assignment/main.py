from pynput import keyboard
from pynput.keyboard import KeyCode
from enum import Enum
from concurrent.futures import ThreadPoolExecutor

from action_msgs.msg import GoalStatus
from std_msgs.msg import String

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import Executor, SingleThreadedExecutor, MultiThreadedExecutor
from rclpy.qos import QoSProfile

from docker import DockManager
from audio_manager import AudioManager
from driver import Drive
from navigator import Navigate
from rotator import Rotate


class FigureFourKeyCommander(Node):

    def __init__(self, key_callbacks=[]):
        super().__init__('figure_four_key_commander')
        self._key_pressed_publisher = self.create_publisher(String, 'key_pressed', 10)

        # add callbacks that are registered with keys
        self._key_callbacks = key_callbacks
        # create a listener for the keyboard that will notify us of presses and releases
        self._listener = keyboard.Listener(
                on_press=self.notify_key_pressed,
                on_release=self.notify_key_released)

        # start the threaded listener
        self._listener.start()

    # stop listening to the keyboard key events
    def stop(self):
        self._listener.stop()

    # callback if a key is pressed 
    def notify_key_pressed(self, key):
        #self.get_logger().info(f'key pressed: {key}')
        # check for callback attached to this key and execute if found
        for key_cb_pair in self._key_callbacks:
            if key_cb_pair[0] == key:
                self.get_logger().info('executing callback attached to key')
                # keys worth taking note of are published
                self.publish_key_pressed(key_cb_pair[0])
                # execute callback
                key_cb_pair[1]()

    # log the key event to the terminal
    def notify_key_released(self, key):
        #self.get_logger().info(f'key released: {key}')
        return

    # notify subscribing nodes which key was pressed
    def publish_key_pressed(self, key):
        self.get_logger().info(f'publishing {key}')
        msg = String()
        msg.data = f'{key}'
        self._key_pressed_publisher.publish(msg)




class FigureFourExecutor(SingleThreadedExecutor):

    class State(Enum):
        DOCKED=0 
        UNDOCKED=1
        LONGSIDE_DONE=2
        TURN_ONE_DONE=3
        ANGLESIDE_DONE=4
        TURN_TWO_DONE=5
        BOTTOM_DONE=6
        TURN_THREE_DONE=7 # spin 360 degrees + amount to go home
        RETURN_DONE=8
        DOCK_DONE=9
        HAPPY=10

    def __init__(self):
        super().__init__()
        self.current_state = self.State.DOCKED
        self.executor_pool = ThreadPoolExecutor(max_workers=1)


    def start(self):
        self.undock_robot()


    def shutdown(self):
        rclpy.shutdown()


    def get_current_state(self):
        print(f'Current State: {self.current_state}')


    def state_transition(self, future=None):
        if future is None:
            print('[WARNING] no transition, current state = {}'.format(self.current_state))
            return self.current_state

        # call the function that manages the current state to create resources (nodes) and then complete the corresponding action
        else: 
            print(f'[INFO] converting future to state')
            # convert future status to state
            if future.result().status == GoalStatus.STATUS_SUCCEEDED:
                self.current_state = self.State(self.current_state.value + 1)
                self.get_current_state()

            else:
                print('[WARNING] goal failed, repeating')

            switcher = {
                self.State.DOCKED: self.undock_robot,
                self.State.UNDOCKED: self.drive_forward,
                self.State.LONGSIDE_DONE: self.turn_one,
                self.State.TURN_ONE_DONE: self.drive_four_angle,
                self.State.ANGLESIDE_DONE: self.turn_two,
                self.State.TURN_TWO_DONE: self.drive_four_base,
                self.State.BOTTOM_DONE: self.turn_three,
                self.State.TURN_THREE_DONE: self.drive_four_home,
                self.State.RETURN_DONE: self.dock,
                self.State.DOCK_DONE: self.play_happy_sounds,
                self.State.HAPPY: self.reset
            }

            ref = switcher.get(self.current_state, 'invalid state')
            if ref is not None or not isinstance(ref, str):
                ref()

            return self.current_state    


    def drive_shape(self):
       self._current_state = 0 


    def spin_once(self):
        try: # wait for callbacks ready to be executed
            handler, group, node = self.wait_for_ready_callbacks(timeout_sec=None)
        except StopIteration:
            pass

        else:
            self.executor_pool.submit(handler)
        



    def undock_robot(self):
        print('[INFO] UNDOCKING ROBOT')

        dock_node = None
        # look for reusable node 
        for node in self.get_nodes():
            if isinstance(node, DockManager):
                print('[INFO] started from pre-made node')
                node.force_send_goal(goal_completed_callbacks=[self.state_transition], assert_docked=True)
                return

        def set_docked():
            self.current_state = self.State.DOCKED

        def set_undocked():
            self.current_state = self.State.UNDOCKED

        # create new node
        dock_man = DockManager(
                lock_node=True, 
                namespace_str='create3_05F8') 
        #        dock_callback=set_docked, 
        #        undock_callback=set_undocked)

        self.add_node(dock_man)
        print('[INFO] started from new node')
        dock_man.force_send_goal(goal_completed_callbacks=[self.state_transition], assert_docked=True)


    def drive_forward(self):
        print('[INFO] DRIVING LONG SIDE')

        for node in self.get_nodes():
            if isinstance(node, Drive):
                node.send_goal(
                    distance=2.0, 
                    velocity=2.25, 
                    goal_completed_callbacks=[self.state_transition]) 
                return

        driver_node = Drive(namespace_str='create3_05F8')
        self.add_node(driver_node)
        driver_node.send_goal(
                distance=2.0, 
                velocity=2.25, 
                goal_completed_callbacks=[self.state_transition]) 


    def turn_one(self):
        print('[INFO] MAKING TURN ONE')
        for node in self.get_nodes():
            if isinstance(node, Rotate):
                node.send_goal(
                    degrees=135, 
                    angular_velocity=1.0, 
                    goal_completed_callbacks=[self.state_transition])
                return

        print('[INFO] creating new rotate node')
        rotate_node = Rotate(namespace_str='create3_05F8')
        self.add_node(rotate_node)
        rotate_node.send_goal(
                    degrees=135, 
                    angular_velocity=1.0, 
                    goal_completed_callbacks=[self.state_transition])


    def drive_four_angle(self):
        print('[INFO] DRIVING ANGLE SIDE')

        for node in self.get_nodes():
            if isinstance(node, Drive):
                node.send_goal(
                    distance=0.2, 
                    velocity=2.25, 
                    goal_completed_callbacks=[self.state_transition]) 
                return

        driver_node = Drive(namespace_str='create3_05F8')
        self.add_node(driver_node)
        driver_node.send_goal(
                distance=0.2, 
                velocity=2.25, 
                goal_completed_callbacks=[self.state_transition]) 


    def turn_two(self):
        print('[INFO] MAKING TURN TWO')
        for node in self.get_nodes():
            if isinstance(node, Rotate):
                node.send_goal(
                    degrees=135, 
                    angular_velocity=1.0, 
                    goal_completed_callbacks=[self.state_transition])
                return

        print('[INFO] creating new rotate node')
        rotate_node = Rotate(namespace_str='create3_05F8')
        self.add_node(rotate_node)
        rotate_node.send_goal(
                    degrees=135, 
                    angular_velocity=1.0, 
                    goal_completed_callbacks=[self.state_transition])



    def drive_four_base(self):
        print('[INFO] DRIVING FOUR BASE')

        for node in self.get_nodes():
            if isinstance(node, Drive):
                node.send_goal(
                    distance=0.2, 
                    velocity=2.25, 
                    goal_completed_callbacks=[self.state_transition]) 
                return

        driver_node = Drive(namespace_str='create3_05F8')
        self.add_node(driver_node)
        driver_node.send_goal(
                distance=0.2, 
                velocity=2.25, 
                goal_completed_callbacks=[self.state_transition]) 


    def turn_three(self):
        print('[INFO] MAKING TURN THREE')
        for node in self.get_nodes():
            if isinstance(node, Rotate):
                node.send_goal(
                    degrees=-360 - 90, 
                    angular_velocity=1.0, 
                    goal_completed_callbacks=[self.state_transition])
                return

        print('[INFO] creating new rotate node')
        rotate_node = Rotate(namespace_str='create3_05F8')
        self.add_node(rotate_node)
        rotate_node.send_goal(
                    degrees=-360 - 90, 
                    angular_velocity=1.0, 
                    goal_completed_callbacks=[self.state_transition])


    def drive_four_home(self):
        print('[INFO] DRIVING FOUR HOME')

        for node in self.get_nodes():
            if isinstance(node, Drive):
                node.send_goal(
                    distance=1.5, 
                    velocity=2.25, 
                    goal_completed_callbacks=[self.state_transition]) 
                return

        driver_node = Drive(namespace_str='create3_05F8')
        self.add_node(driver_node)
        driver_node.send_goal(
                distance=1.5, 
                velocity=2.25, 
                goal_completed_callbacks=[self.state_transition]) 


    def dock(self):
        print('[INFO] DOCKING')

        dock_node = None
        # look for reusable node 
        for node in self.get_nodes():
            if isinstance(node, DockManager):
                print('[INFO] started from pre-made node')
                node.force_send_goal(goal_completed_callbacks=[self.state_transition], assert_docked=False)
                return

        def set_docked():
            self.current_state = self.State.DOCKED

        def set_undocked():
            self.current_state = self.State.UNDOCKED

        # create new node
        dock_man = DockManager(
                lock_node=True, 
                namespace_str='create3_05F8') 

        self.add_node(dock_man)
        print('[INFO] started from new node')
        dock_man.force_send_goal(goal_completed_callbacks=[self.state_transition], assert_docked=False)


    def play_happy_sounds(self):
        print('[INFO] PLAYING HAPPY SOUNDS')

        for node in self.get_nodes():
            if isinstance(node, AudioManager):
                node.send_goal()


        audio_manager = AudioManager(namespace_str='create3_05F8')
        audio_manager.send_goal()


    def reset(self):
        print('[INFO] RESETTING STATE')


def main(args=None):
    rclpy.init(args=args)

    executor = FigureFourExecutor()

    keycomand_node = FigureFourKeyCommander(key_callbacks=[
                        (KeyCode(char='s'), executor.shutdown),
                        (KeyCode(char='w'), executor.start),
                        (KeyCode(char='u'), executor.get_current_state)])

    executor.add_node(keycomand_node)

    executor.spin()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
