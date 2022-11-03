import rclpy

from robot import RobotLogic

def main(args=None):
    rclpy.init(args=args)
    robot = RobotLogic(robot_id="create3_05B9", mqtt_ip="localhost")
    robot.start()

if __name__ == "__main__":
    main()
