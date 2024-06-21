import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial


class CmdVelReader(Node):

    def __init__(self):
        super().__init__('cmd_vel_reader')

        self.declare_parameter('subscription_topic', '/cmd_vel')
        self.subscription_topic = self.get_parameter('subscription_topic').value

        self.subscription = self.create_subscription(
            Twist,
            self.subscription_topic,
            self.cmd_vel_callback,
            10
        )
        self.get_logger().info(f"Subscribed to topic: {self.subscription_topic}")

        self.declare_parameter('serial_port', '/dev/ttyUSB0')
        self.serial_port = self.get_parameter('serial_port').value
        
        self.declare_parameter('baud_rate', 57600)
        self.baud_rate = self.get_parameter('baud_rate').value

        self.conn = serial.Serial(self.serial_port, self.baud_rate, timeout=1.0)
        self.get_logger().info(f"Connected to Arduino on port: {self.serial_port} at baud rate: {self.baud_rate}")

    def send_pwm_to_arduino(self, pwm_left, pwm_right, pwm_vertical):
        # Format the command string
        command = f"{pwm_left},{pwm_right},{pwm_vertical}\n"
        self.conn.write(command.encode())
        if self.get_logger().get_effective_level() <= rclpy.logging.LoggingSeverity.DEBUG:
            self.get_logger().debug(f"Sent to Arduino: {command.strip()}")
            
    def cmd_vel_callback(self, msg):
        # Read the velocities
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        linear_z = msg.linear.z


        left_speed = 0
        right_speed = 0
        if linear_x >= 0 and angular_z <= 0:
            left_speed = max(linear_x, abs(angular_z))
            if(linear_x <= 0.5):
                right_speed = linear_x
            else:
                right_speed = linear_x + angular_z / 2
        elif linear_x >= 0 and angular_z >= 0:
            right_speed = max(linear_x, angular_z)
            if linear_x <= 0.5:
                left_speed = linear_x
            else:
                left_speed = linear_x - angular_z / 2
        elif linear_x <= 0 and angular_z <= 0:
            right_speed = 0
            left_speed = 0

        elif linear_x <= 0 and angular_z >= 0:
            left_speed = 0
            right_speed = 0

        pwm_left = self.convert_to_pwm(left_speed)
        pwm_right = self.convert_to_pwm(right_speed)
        pwm_vertical = self.convert_to_pwm(linear_z)

        # Print the PWM values
        self.get_logger().info(f"PWM Left: {pwm_left}, PWM Right: {pwm_right}, PWM Vertical: {pwm_vertical}")

        # Send the PWM values to Arduino
        self.send_pwm_to_arduino(pwm_left, pwm_right, pwm_vertical)

    def convert_to_pwm(self, velocity):
        if velocity <= 0:
            return 0
        elif velocity >= 1:
            return 255
        else:
            return int(velocity * 255)

def main(args=None):
    rclpy.init(args=args)
    cmd_vel_reader = CmdVelReader()
    rclpy.spin(cmd_vel_reader)
    cmd_vel_reader.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
