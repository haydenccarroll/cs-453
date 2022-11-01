from undock_driver import UndockDriver
import rclpy

from odom_sub import OdomSub
from state_setter import StateMachine
from detections_sub import DetectionsSub
from robot_subs import RobotSubs
from goal_driver import GoalDriver
from reset_pose_driver import ResetPoseDriver
from collision_driver import CollisionDriver

from paho.mqtt import client as mqtt
from enum import IntEnum
from geometry_msgs.msg import PoseStamped
import time
import math

class InternalState(IntEnum):
    DOINGCOLLISION=0,
    ATGOAL=1
    OTHER=2

class RobotLogic():
    def __init__(self, robot_id, mqtt_ip):
        self.mqtt_client = mqtt.Client(f"{robot_id} mqtt client")
        self.mqtt_client.connect(mqtt_ip)

        self.robot_id = robot_id
        self.old_collision = None
        self.odom_sub = OdomSub(robot_id, self.mqtt_client)
        self.detections_sub = DetectionsSub(robot_id, self.mqtt_client)
        self.all_robots = RobotSubs(["create3_05B9", "create3_05B9"], self.mqtt_client)

        self.external_state = StateMachine(robot_id, self.mqtt_client)
        self.internal_state = InternalState.OTHER

        goal_pose = PoseStamped()
        goal_pose.pose.position.x = 0.0
        goal_pose.pose.position.y = 0.0
        goal_pose.pose.position.z = 0.0
        goal_pose.pose.orientation.x = 0.0
        goal_pose.pose.orientation.y = 0.0
        goal_pose.pose.orientation.z = 0.0
        goal_pose.pose.orientation.w = 1.0



        self.goal_driver = GoalDriver(robot_id, goal_pose)
        self.collision_driver = CollisionDriver(robot_id)
        self.reset_pose_driver = ResetPoseDriver(robot_id)
        self.undock_driver = UndockDriver(robot_id)

    def collisionDetection(self):
        print(self.all_robots.get_robot(self.robot_id).pose)
        our_position = self.all_robots.get_robot(self.robot_id).pose.position
        for robot in self.all_robots.get_robots():
            if robot.id == self.robot_id:
                continue

            robot_position = robot.pose.position
            robot_velocity = robot.pose.twist.velocity

            # angle from our position and robot position
            angle = math.atan2(robot_position.y - our_position.y,
                               robot_position.x - our_position.x)

            # offsetting the angle by the way we are facing
            angle -= our_position.orientation.angle
            angle %= math.pi * 2
            lower_bound = math.pi / 4
            upper_bound = math.pi * 3 / 4
            if not (lower_bound <= angle <= upper_bound):
                continue
            
            robot_velocity = robot.twist.velocity
            if math.dist(robot_position, our_position) <= 0.5 * robot_velocity:
                return robot.id
        return None

    def start(self):
        # undock (blocking)
        self.undock_driver.startBlocking()
        print("UNDOCK SHOULD BE DONE!")
        # reset pose (blocking)
        self.reset_pose_driver.start()
        print("RESET POSE SHOULD BE DONE!")
        # start moving to goal (nonblocking)
        self.goal_driver.start()
        while rclpy.ok():
            print("SPINNING")
            # spinning on mqtt pub/sub nodes
            rclpy.spin_once(self.detections_sub, timeout_sec=0)
            rclpy.spin_once(self.odom_sub, timeout_sec=0)
            rclpy.spin_once(self.external_state, timeout_sec=0)
            self.external_state.send_state_to_mqtt()
            self.all_robots.update_robots_pos()


            done, _ = self.goal_driver.spin()
            if done:
                self.internal_state = InternalState.ATGOAL
                print("GOAL IS DONE")


            done, _ = self.collision_driver.spin()
            
            if done: # on end of collision avoidance routine
                self.internal_state = InternalState.OTHER
                self.goal_driver.start()
                self.old_collision = None



            # if there is a collision
            if newCollision := self.collisionDetection() is not None:
                print("THERE IS A COLLISION")
                self.goal_driver.stop()

                # just started a brand new collision
                if self.internal_state == InternalState.OTHER:
                    # turn left 90deg to start.
                    #TODO: this is the wrong amount of degrees. it shuld first match  
                    self.collision_driver.start(- 1 * math.pi / 4)
                self.internal_state = InternalState.DOINGCOLLISION

                # if another collision while doing collision
                if newCollision != self.oldCollision and self.oldCollision is not None:
                    self.old_collision = newCollision
                    self.collision_driver.reset()

            time.sleep(0.1)
