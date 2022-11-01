from rclpy.node import Node

from paho.mqtt import client as mqtt

from enum import IntEnum

class State(IntEnum):
    OCCLUDED=0,
    PERAMBULATING=1,
    CONCUSSED=2,
    DYING=3,
    RANDR=4,
    ALIENS=5

class StateMachine(Node):
    def __init__(self, robot_name, mqtt_client):
        super().__init__(f"{robot_name}_state_machine_node")
        self.mqtt_client = mqtt_client
        self.robot_id = robot_name

        self.isKidnapped = False
        self.isLowBattery = False
        self.isDocked = False
        self.isMoving = False
        self.isCovHigh = False

        self.state = State.PERAMBULATING

    def getState(self):
        return self.state

    def send_state_to_mqtt(self):
        state = State.PERAMBULATING
        if self.isDocked:
            state = State.RANDR
        elif self.isKidnapped:
            state = State.ALIENS
        elif self.isLowBattery:
            state = State.DYING
        else:
            if self.isCovHigh:
                if self.isMoving:
                    state = State.OCCLUDED
                else:
                    state = State.CONCUSSED
        
        self.mqtt_client.publish(
            f"irobot_create3_swarm/robot_status/{self.robot_id}",
            int(state))
        self.state = state
        return self.state
