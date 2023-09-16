#!/usr/bin/python3

import rclpy
from rclpy.node import Node

# Import Message Types
from geometry_msgs.msg import Twist # Twist - cmd_vel
from turtlesim.msg import Pose      # Pose  - pose
from turtlesim_plus_interfaces.srv import GivePosition
from std_srvs.srv import Empty      # Empty  
from std_msgs.msg import Bool

# Import Service Interface
from turtlesim_plus_control_interfaces.srv import SetTarget

# Import Other Associated Libraries
from math import atan2, hypot, sin, cos

class controller(Node):
    def __init__(self):
        super().__init__('controller')

        self.declare_parameter('linear_gain', 1.0)
        self.declare_parameter('angular_gain', 10.0)
        self.declare_parameter('tolerance', 0.2)

        # Create Publisher & Timer to publish
        self.pub_cmd_vel = self.create_publisher(Twist,'cmd_vel', 10)
        self.pub_finished_alphabet = self.create_publisher(Bool,'finished_alphabet', 10)
        self.create_timer(0.01, self.timer_callback)
        
        # Create Subscriber
        self.create_subscription(Pose, 'pose', self.pose_callback, 10)

        # Create Service Server
        self.create_service(SetTarget, "set_goal", self.set_goal_callback)
        self.create_service(Empty, "finish_alphabet_notification", self.finish_alphabet_notification_callback)

        # Create Service Client
        self.arrived_notification_client = self.create_client(Empty, "arrived_notification")
        self.spawn_pizza_client = self.create_client(GivePosition, "/spawn_pizza")

        # Create Class variables
        self.turtle_pose = [0.0, 0.0, 0.0]
        self.target_pos = [0.0, 0.0]
        self.controller_enable = False
        self.enable_alphabet = True
        self.start_up_flag = True
        self.timestamp = 0.00
        self.linear_gain = self.get_parameter('linear_gain').get_parameter_value().double_value
        self.angular_gain = self.get_parameter('angular_gain').get_parameter_value().double_value
        self.tolerance = self.get_parameter('tolerance').get_parameter_value().double_value

    # Timer Callback =================================
    def timer_callback(self):
        msg = Bool()
        msg.data = not self.enable_alphabet
        self.pub_finished_alphabet.publish(msg)
        if self.start_up_flag:
            self.timestamp = self.timestamp + 0.01
            if self.timestamp >= 5:
                self.arrived_notify()
                self.start_up_flag = False
        if self.controller_enable:
            self.controller()

    # Topics =========================================
    # Subscriber Callback
    def pose_callback(self, msg):
        self.turtle_pose = [msg.x, msg.y, msg.theta]

    # Publish Function
    def cmd_vel_pub(self, vx:float, w:float)->None:
        cmd_vel = Twist()
        cmd_vel.linear.x = vx
        cmd_vel.angular.z = w
        self.pub_cmd_vel.publish(cmd_vel)

    # Services =======================================
    # Service Server Callback
    def set_goal_callback(self, req, res):
        self.target_pos = [req.target.x, req.target.y]
        self.controller_enable = True
        return SetTarget.Response()
    
    def finish_alphabet_notification_callback(self, req, res):
        self.enable_alphabet = False
        return Empty.Response()

    # Service Client Request
    def arrived_notify(self):
        req = Empty.Request()
        self.arrived_notification_client.call_async(req)
    
    def spawn_pizza(self):
        position_request = GivePosition.Request()
        position_request.x = self.turtle_pose[0]
        position_request.y = self.turtle_pose[1]
        self.spawn_pizza_client.call_async(position_request)
    
    # Controller =====================================
    def controller(self)->None:
        dx = self.target_pos[0] - self.turtle_pose[0]
        dy = self.target_pos[1] - self.turtle_pose[1]
        target_theta = atan2(dy,dx)
        diff_dis = hypot(dy,dx)
        
        if diff_dis < self.tolerance:
            self.controller_enable = False
            self.cmd_vel_pub(0.0,0.0)
            self.arrived_notify()
            if self.enable_alphabet:
                self.spawn_pizza()

        else:
            diff_theta = target_theta - self.turtle_pose[2]
            diff_theta = atan2(sin(diff_theta),cos(diff_theta))
            vx = self.linear_gain * diff_dis
            w = self.angular_gain * diff_theta
            self.cmd_vel_pub(vx, w)


def main(args=None):
    rclpy.init(args=args)
    node = controller()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()