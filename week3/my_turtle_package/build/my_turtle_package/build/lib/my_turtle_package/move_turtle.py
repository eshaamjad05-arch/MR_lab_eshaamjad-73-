#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn

class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')

        # Keep track of turtle publishers
        self.my_publishers = {}  # <-- renamed

        # Spawn turtles
        self.spawn_turtle('turtle1', 2.0, 2.0, 0.0)
        self.spawn_turtle('turtle2', 5.0, 5.0, 0.0)
        self.spawn_turtle('turtle3', 8.0, 8.0, 0.0)

        # State trackers for square/triangle steps
        self.square_step = 0
        self.triangle_step = 0
        self.angle_accum1 = 0.0
        self.angle_accum3 = 0.0

        # Timers for continuous movement
        self.create_timer(0.1, self.move_square_turtle1)
        self.create_timer(0.1, self.move_circle_turtle2)
        self.create_timer(0.1, self.move_triangle_turtle3)

    def spawn_turtle(self, name, x, y, theta):
        client = self.create_client(Spawn, 'spawn')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for spawn service...')
        req = Spawn.Request()
        req.x = x
        req.y = y
        req.theta = theta
        req.name = name
        future = client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        # Add publisher to the renamed dictionary
        self.my_publishers[name] = self.create_publisher(Twist, f'{name}/cmd_vel', 10)
        self.get_logger().info(f'{name} spawned at ({x}, {y})')

    # Continuous square movement
    def move_square_turtle1(self):
        pub = self.my_publishers['turtle1']
        msg = Twist()
        if self.square_step % 2 == 0:
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.angle_accum1 += 0.1
            if self.angle_accum1 > 2.0:  # Move forward for some time
                self.angle_accum1 = 0.0
                self.square_step += 1
        else:
            msg.linear.x = 0.0
            msg.angular.z = 1.57  # Turn 90 degrees
            self.angle_accum1 += 0.1
            if self.angle_accum1 > 1.57:
                self.angle_accum1 = 0.0
                self.square_step += 1
        pub.publish(msg)

    # Continuous circle movement
    def move_circle_turtle2(self):
        pub = self.my_publishers['turtle2']
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0
        pub.publish(msg)

    # Continuous triangle movement
    def move_triangle_turtle3(self):
        pub = self.my_publishers['turtle3']
        msg = Twist()
        if self.triangle_step % 2 == 0:
            msg.linear.x = 2.0
            msg.angular.z = 0.0
            self.angle_accum3 += 0.1
            if self.angle_accum3 > 2.0:
                self.angle_accum3 = 0.0
                self.triangle_step += 1
        else:
            msg.linear.x = 0.0
            msg.angular.z = 2.09  # 120 degrees turn
            self.angle_accum3 += 0.1
            if self.angle_accum3 > 2.09:
                self.angle_accum3 = 0.0
                self.triangle_step += 1
        pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    controller = TurtleController()
    try:
        rclpy.spin(controller)  # Keep the node running
    except KeyboardInterrupt:
        pass
    controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
