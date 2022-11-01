import time
import rclpy

from hw1_assignment.undock import UndockNode
from hw1_assignment.dock import DockNode
from hw1_assignment.forward import ForwardNode
from hw1_assignment.turn import TurnNode
from hw1_assignment.noise import NoiseNode



def figure_4(d_node, o_node):
    pass

def main(args=None):
    rclpy.init(args=args)

    robotName = "create3_05B9"
    undock_node = UndockNode(robotName)
    dock_node = DockNode(robotName)
    forward_node = ForwardNode(robotName)
    turn_node = TurnNode(robotName)
    noise_node = NoiseNode(robotName)

    done, accepted = undock_node.do()
    time.sleep(1)
    done, accepted = forward_node.do(2, 1)
    time.sleep(1)
    done, accepted = forward_node.do(0.75, 1)
    time.sleep(1)
    done, accepted = turn_node.do(135, 0.1)
    time.sleep(1)
    done, accepted = forward_node.do(0.5, 1)
    time.sleep(1)
    done, accepted = turn_node.do(135, 0.1)
    time.sleep(1)
    done, accepted = forward_node.do(0.5, 1)
    time.sleep(1)
    done, accepted = turn_node.do(360, 0.1)
    time.sleep(1)
    done, accepted = turn_node.do(-95, 0.1)
    time.sleep(1)
    done, accepted = forward_node.do(2.2, 1)
    time.sleep(1)
    done, accepted = dock_node.do()
    time.sleep(1)
    done, accepted = noise_node.do()

    rclpy.shutdown()