import hw1_assignment.drive_node
import hw1_assignment.odom_node

import rclpy
import threading

def main(args=None):
    rclpy.init(args=args)
    d_node = hw1_assignment.drive_node.DriveNode("create3_05F8")
    o_node = hw1_assignment.odom_node.OdomNode("create3_05F8")
    rclpy.spin_once(o_node)

    print("HELLO DOES IT PRINT AFTER A SPIN", flush=True)

    # drive_node.undock()
    while o_node.pose.position.x - 2 < 0:
        # print(o_node.pose.position)
        d_node.drive_forward()
        rclpy.spin_once(o_node)
        pass
    
    d_node.figure4()
    d_node.spinaround()
    d_node.movetodock()
    d_node.dock()


    d_node.destroy_node()
    rclpy.shutdown()