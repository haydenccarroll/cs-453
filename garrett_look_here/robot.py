from undock_driver import UndockDriver
import rclpy

from odom_sub import OdomSub
from state_setter import StateMachine
from detections_sub import DetectionsSub
from robot_subs import RobotSubs
from goal_driver import GoalDriver
from reset_pose_driver import ResetPoseDriver
from collision_driver import CollisionDriver
from beep_driver import BeepDriver

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
        self.odom_sub = OdomSub(robot_id, mqtt_ip)
        self.detections_sub = DetectionsSub(robot_id, mqtt_ip)
        self.all_robots = RobotSubs(["create3_05B9", "dummy", "create3_05F8", "create3_05AE", "create3_0620"], mqtt_ip)

        self.external_state = StateMachine(robot_id, mqtt_ip)
        self.internal_state = InternalState.OTHER

        self.goal_pose = PoseStamped()
        self.goal_pose.pose.position.x = 1.8
        self.goal_pose.pose.position.y = 0 - 1.926
        self.goal_pose.pose.position.z = 0.0
        self.goal_pose.pose.orientation.x = 0.0
        self.goal_pose.pose.orientation.y = 0.0
        self.goal_pose.pose.orientation.z = 0.0
        self.goal_pose.pose.orientation.w = 1.0



        self.goal_driver = GoalDriver(robot_id)
        self.collision_driver = CollisionDriver(robot_id)
        self.reset_pose_driver = ResetPoseDriver(robot_id)
        self.undock_driver = UndockDriver(robot_id)
        self.beep_driver = BeepDriver(robot_id)

    def isInBounds(self):
        pos = self.all_robots.get_robot(self.robot_id).pose
        if pos is None:
            return True

        xcoord = pos["position"]["x"]
        ycoord = pos["position"]["y"]
        if not (-0.2 <= xcoord and xcoord <= 2):
            return False
        if not (-0.3 <= ycoord and ycoord <= 2.3):
            return False

        return True

    def collisionDetection(self):
        def magnitude(vector):
            return math.sqrt(sum(pow(element, 2) for element in vector))
        our_robot = self.all_robots.get_robot(self.robot_id)
        if our_robot.pose is None: # we cant check for collision, we dont have our pos
            return False, 0
        for robot in self.all_robots.get_robots():
            if robot.id == self.robot_id or robot.pose is None:
                continue

            robot_position = robot.pose["position"]
            robot_velocity = magnitude([robot.twist["linear"]["x"],
                                        robot.twist["linear"]["y"],
                                        robot.twist["linear"]["z"]])

            ''' DELETE THIS SECTION vvvv'''
            ourRot = our_robot.pose["rotation"]["z"] * math.pi
             # angle from our position and robot position
            angle = math.atan2(robot_position["y"] - our_robot.pose["position"]["y"],
                               robot_position["x"] - our_robot.pose["position"]["x"])
            # offsetting the angle by the way we are facing
            angle -= ourRot
            
   
            lower_bound = - math.pi / 3
            upper_bound = math.pi / 3
            if not (lower_bound <= angle <= upper_bound):
                continue

            robot_distance = math.dist((robot_position["x"], robot_position["y"]), 
                         (our_robot.pose["position"]["x"], our_robot.pose["position"]["y"]))

            if robot_distance <= 0.5 + 0.2 * robot_velocity:
                return robot.id, angle
        return (False, 0)

    def start(self):
        # undock (blocking)
        self.undock_driver.startBlocking()
        print("UNDOCK SHOULD BE DONE!")
        # reset pose (blocking)
        self.reset_pose_driver.start()
        print("RESET POSE SHOULD BE DONE!")

        while (self.all_robots.get_robot(self.robot_id).pose) is None:
            rclpy.spin_once(self.odom_sub, timeout_sec=0)

        pose = self.all_robots.get_robot(self.robot_id).pose
        self.goal_pose.pose.orientation.x = pose["rotation"]["x"]
        self.goal_pose.pose.orientation.y = pose["rotation"]["y"]
        self.goal_pose.pose.orientation.z = pose["rotation"]["z"]
        self.goal_pose.pose.orientation.w = pose["rotation"]["w"]


        # start moving to goal (nonblocking)
        self.goal_driver.start(self.goal_pose)
        while rclpy.ok():
            # spinning on mqtt pub/sub nodes
            rclpy.spin_once(self.odom_sub, timeout_sec=0)
            rclpy.spin_once(self.detections_sub, timeout_sec=0)
            rclpy.spin_once(self.external_state, timeout_sec=0)
            rclpy.spin_once(self.all_robots, timeout_sec=0)
            self.external_state.send_state_to_mqtt()

            # if InternalState.ATGOAL:
            #     continue


            done, accepted = self.goal_driver.spin()
            if done:
                print("DONE")
                self.internal_state = InternalState.ATGOAL
                # rclpy.shutdown()


            done, _ = self.collision_driver.spin()
            if done and self.internal_state == InternalState.DOINGCOLLISION: 
            # on end of collision avoidance routine
                print("COLLISION ROUTINE DONE")
                self.internal_state = InternalState.OTHER
                self.goal_driver.start(self.goal_pose)
                self.old_collision = None


            # if there is a collision
            newCollision, angle = self.collisionDetection()
            if (newCollision) is not False or not self.isInBounds():
                if not self.isInBounds():
                    newCollision = "WALL"
                self.goal_driver.stop()
                print("THERE IS A COLLISION: ", newCollision)


                # just started a brand new collision
                if self.internal_state == InternalState.OTHER:
                    self.beep_driver.startBlocking()

                    # turn left 90deg to start.
                    self.collision_driver.start(angle + math.pi / 2)
                self.internal_state = InternalState.DOINGCOLLISION

                # if another collision while doing collision
                if newCollision != self.old_collision and self.old_collision is not None:
                    self.old_collision = newCollision
                    self.collision_driver.reset()

