import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class CameraFollower(Node):

    def __init__(self):
        super().__init__('camera_follower')

        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)

        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.bridge = CvBridge()

        # CONTROL
        self.kp_ang = 0.0012
        self.max_ang = 0.3

        self.linear_speed = 0.15
        self.slow_speed = 0.06

        # ALIGNMENT
        self.align_thresh = 8   # tighter accuracy
        self.min_area = 800
        self.stop_area = 900000

        self.spin_spd = 0.25

        # smoothing filter (VERY IMPORTANT)
        self.prev_cx = None
        self.alpha = 0.6   # smoothing factor

        self.get_logger().info("Stable Centroid Tracker Started")

    def image_callback(self, msg):

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        h, w, _ = frame.shape
        cx_frame = w // 2

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.bitwise_or(
            cv2.inRange(hsv, np.array([0, 120, 70]), np.array([10, 255, 255])),
            cv2.inRange(hsv, np.array([170, 120, 70]), np.array([180, 255, 255]))
        )

        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cmd = Twist()

        if contours:

            largest = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest)

            if area > self.min_area:

                M = cv2.moments(largest)

                if M["m00"] != 0:

                    cx_raw = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # 🔥 SMOOTH CENTROID (KEY FIX)
                    if self.prev_cx is None:
                        cx = cx_raw
                    else:
                        cx = int(self.alpha * self.prev_cx + (1 - self.alpha) * cx_raw)

                    self.prev_cx = cx

                    error = cx_frame - cx

                    # ================= ALIGN =================
                    if abs(error) > self.align_thresh:
                        cmd.linear.x = 0.0
                        cmd.angular.z = max(
                            -self.max_ang,
                            min(self.max_ang, self.kp_ang * error)
                        )

                    # ================= APPROACH =================
                    else:
                        cmd.angular.z = 0.0

                        if area >= self.stop_area:
                            cmd.linear.x = 0.0
                        else:
                            # closer → slower
                            cmd.linear.x = self.linear_speed * (1 - area/self.stop_area)

                    # VISUALIZATION
                    cv2.circle(frame, (cx, cy), 8, (0,0,255), -1)
                    cv2.line(frame, (cx_frame, 0), (cx_frame, h), (255,255,255), 1)

                    cv2.putText(frame,
                        f"err={error} area={int(area)}",
                        (10,30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0,255,0),
                        2)

        else:
            cmd.angular.z = self.spin_spd
            cmd.linear.x = 0.0

            self.prev_cx = None

        self.pub.publish(cmd)

        cv2.imshow("Camera", frame)
        cv2.imshow("Mask", mask)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = CameraFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
