#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute
import math

class TurtleGoto(Node):
    def __init__(self):
        super().__init__('turtle_goto')
        self.publisher = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)

        # Target coordinates
        self.target_x = 5.0
        self.target_y = 5.0

        # Timer to control movement
        self.create_timer(0.1, self.move_to_target)

    def move_to_target(self):
        msg = Twist()
        # Get current position
        # For simplicity, we can teleport turtle first or use odometry in advanced version
        # Here we just send a simple velocity command
        # This example moves turtle diagonally to target
        msg.linear.x = 1.5
        msg.angular.z = 0.0
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = TurtleGoto()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
