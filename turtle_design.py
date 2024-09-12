#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.srv import Spawn, Kill
import time
import math
import subprocess  # To start turtlesim node

class TurtleGanesha(Node):

    def __init__(self):
        super().__init__('turtle_ganesha')

        # Start turtlesim node in the background
        self.start_turtlesim()
        time.sleep(1)

        # Kill the existing turtle1
        self.kill_turtle('turtle1')
        time.sleep(1)

        # Call the spawn service to reposition the turtle
        self.spawn_turtle(7.5, 5.5, 0.0)  # Spawn turtle at a custom position

        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 30)
        time.sleep(2)  # Wait for the connection to be established
        
        self.create_design()

        self.kill_turtle('turtle1')
        time.sleep(1)

        self.spawn_turtle(6.1, 2.46, 0.0)
        time.sleep(1)

        self.create_design2()

        self.kill_turtle('turtle1')
        time.sleep(1)

        self.spawn_turtle(5.8, 7.0, 0.0)
        time.sleep(1)

        self.create_design3()

        self.kill_turtle('turtle1')
        time.sleep(1)

        self.spawn_turtle(7.3, 7.7, 0.0)
        time.sleep(1)

        self.create_design4()

        self.kill_turtle('turtle1')
        time.sleep(1)

        self.spawn_turtle(7.2, 8.1, 0.0)
        time.sleep(1)

        self.create_design5()

        self.kill_turtle('turtle1')
        time.sleep(1)

        self.spawn_turtle(5.5, 9.0, 0.0)
        time.sleep(1)

        self.create_design6()

        self.kill_turtle('turtle1')



    def start_turtlesim(self):
        """Start the turtlesim node."""
        self.get_logger().info('Starting turtlesim node...')
        subprocess.Popen(['ros2', 'run', 'turtlesim', 'turtlesim_node'])
        time.sleep(2)  # Give it a moment to launch

    def kill_turtle(self, name):
        """Kill the existing turtle by name (e.g., turtle1)."""
        client = self.create_client(Kill, '/kill')

        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /kill not available, waiting...')

        request = Kill.Request()
        request.name = name

        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f'Turtle [{name}] killed successfully.')
        else:
            self.get_logger().error(f'Failed to kill turtle [{name}].')

    def spawn_turtle(self, x, y, theta):
        """Spawn the turtle at a new position (x, y) with orientation theta."""
        client = self.create_client(Spawn, '/spawn')

        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service /spawn not available, waiting...')

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = theta
        request.name = 'turtle1'

        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f'Turtle spawned at {x}, {y}')
        else:
            self.get_logger().error('Failed to spawn turtle')

    def move_forward(self, speed, distance):
        velocity_msg = Twist()
        velocity_msg.linear.x = speed

        t0 = time.time()
        current_distance = 0.0

        while current_distance < distance:
            self.publisher_.publish(velocity_msg)
            t1 = time.time()
            current_distance = speed * (t1 - t0)

        velocity_msg.linear.x = 0.0
        self.publisher_.publish(velocity_msg)

    def rotate(self, angular_speed, angle, clockwise=True):
        velocity_msg = Twist()
        if clockwise:
            velocity_msg.angular.z = -abs(angular_speed)
        else:
            velocity_msg.angular.z = abs(angular_speed)

        t0 = time.time()
        current_angle = 0.0

        while current_angle < angle:
            self.publisher_.publish(velocity_msg)
            t1 = time.time()
            current_angle = angular_speed * (t1 - t0)

        velocity_msg.angular.z = 0.0
        self.publisher_.publish(velocity_msg)

    def draw_smooth_curve(self, radius, angle, segments):
        """Draw a smooth curve by breaking it into small segments."""
        segment_angle = angle / segments
        segment_distance = (2 * math.pi * radius * (segment_angle / 360))

        for _ in range(segments):
            self.move_forward(0.5, segment_distance)
            self.rotate(1.0, math.radians(segment_angle), clockwise=False)

    def draw_smooth_curve_opposite(self, radius, angle, segments):
        """Draw a smooth curve by breaking it into small segments."""
        segment_angle = angle / segments
        segment_distance = (2 * math.pi * radius * (segment_angle / 360))

        for _ in range(segments):
            self.move_forward(0.5, segment_distance)
            self.rotate(1.0, math.radians(segment_angle), clockwise=True)

    def draw_ear_left(self):
        """Draw the left ear using smooth curves."""
        self.rotate(1.0, math.radians(50), clockwise=True)
        self.move_forward(0.5, 0.5)
        self.draw_smooth_curve(0.3, 110, 30)
        self.rotate(1.0, math.radians(15), clockwise=False)
        self.move_forward(0.5, 0.5)
        self.rotate(1.0, math.radians(10), clockwise=True)
        self.move_forward(0.5, 2.0)
        self.rotate(1.0, math.radians(80), clockwise=False)
        self.move_forward(0.5, 0.2)
        self.draw_smooth_curve(1.3, 120, 30)
        
        
    def draw_trunk(self):
        """Draw the trunk with a long curve and spiral."""
        self.rotate(1.0, math.radians(2), clockwise=False)
        self.move_forward(0.5, 1.7)
        self.draw_smooth_curve_opposite(1.3, 45, 30)
        self.rotate(1.0, math.radians(12), clockwise=False)
        self.move_forward(0.5, 1.0)
        self.draw_smooth_curve(0.5, 185, 30)
        self.rotate(1.0, math.radians(180), clockwise=True)
        self.draw_smooth_curve_opposite(0.85, 185, 30)
        self.rotate(1.0, math.radians(5), clockwise=False)
        self.move_forward(0.5, 0.4)
        self.draw_smooth_curve(2.0, 50, 30)
        self.rotate(1.0, math.radians(10), clockwise=True)
        self.move_forward(0.5, 1.0)


    def draw_ear_right(self):
        """Draw the right ear."""
        self.rotate(1.0, math.radians(30), clockwise=False)
        self.move_forward(0.5, 0.5)
        self.draw_smooth_curve(1.0, 90, 30)
        self.move_forward(0.5, 0.5)
        self.move_forward(0.5, 0.3)
        self.rotate(1.0, math.radians(100), clockwise=False)
        self.draw_smooth_curve_opposite(4.0, 35, 30)
        self.rotate(1.0, math.radians(110), clockwise=False)
        self.draw_smooth_curve(1.0, 60, 30)
        
        

    def draw_crown(self):
        """Draw a few simple arcs for the crown."""
        self.rotate(1.0, math.radians(150), clockwise=False)
        self.draw_smooth_curve(3.0, 50, 30)

    def draw_crown2(self):
        """Draw a few simple arcs for the crown."""
        self.rotate(1.0, math.radians(150), clockwise=False)
        self.draw_smooth_curve(2.9, 50, 30)


    def draw_bindi(self):
        """Draw a small circle for the bindi."""
        self.rotate(1.0, math.radians(75), clockwise=True)
        self.draw_smooth_curve(0.1, 180, 20)
        self.move_forward(0.5, 0.5)
        self.rotate(1.0, math.radians(160), clockwise=False)
        self.move_forward(0.5, 0.5)

    def draw_bindi2(self):
        """Draw a small circle for the bindi."""
        self.rotate(1.0, math.radians(75), clockwise=True)
        self.draw_smooth_curve(0.3, 180, 20)
        self.rotate(1.0, math.radians(10), clockwise=False)
        self.move_forward(0.5, 0.55)
        self.rotate(1.0, math.radians(130), clockwise=False)
        self.move_forward(0.5, 0.68)

    def create_design(self):
        """Draw the full Ganesha design."""
        self.draw_ear_left()  
        self.draw_trunk()     
        self.draw_ear_right() 


    def draw_modak(self):
        """Draw the round modak"""
        self.draw_smooth_curve(0.25, 360, 30)


    def create_design2(self):
        self.draw_modak()

    def create_design3(self):
        self.draw_bindi()     # Draw the bind

    def create_design4(self):
        self.draw_crown()

    def create_design5(self):
        self.draw_crown2()

    def create_design6(self):
        self.draw_bindi2()

def main(args=None):
    rclpy.init(args=args)
    turtle_ganesha = TurtleGanesha()
    rclpy.spin(turtle_ganesha)
    turtle_ganesha.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
