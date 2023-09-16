#!/usr/bin/python3

import rclpy
from rclpy.node import Node

# Import Message Types
from geometry_msgs.msg import Point # Point - set_goal
from std_srvs.srv import Empty      # Empty - 
from std_msgs.msg import Bool

# Import Service Interface 
from turtlesim_plus_control_interfaces.srv import SetTarget

# Import Other Associated Libraries
from ament_index_python import get_package_share_directory
from time import sleep
import yaml
import os

class scheduler(Node):
    def __init__(self):
        super().__init__('scheduler')

        self.create_subscription(Bool, '/finished', self.finish_callback, 10)
        
        # Create Service Server
        self.create_service(Empty, "arrived_notification", self.arrived_notification_callback)

        # Create Service Client
        self.set_goal_client = self.create_client(SetTarget, "set_goal")
        self.finish_alphabet_notification_client = self.create_client(Empty, "finish_alphabet_notification")
        
        # Get viapoint path for each turtle
        self.namespace = self.get_namespace()

        turtlesim_plus_control_pkg = get_package_share_directory('turtlesim_plus_control')
        self.viapoint_path = os.path.join(turtlesim_plus_control_pkg,'viapoint','via_point_01.yaml')

        if self.namespace == "/Foxy":
            self.viapoint_path = os.path.join(turtlesim_plus_control_pkg,'viapoint','via_point_F.yaml')
        elif self.namespace == "/Noetic":
            self.viapoint_path = os.path.join(turtlesim_plus_control_pkg,'viapoint','via_point_I.yaml')
        elif self.namespace == "/Humble":
            self.viapoint_path = os.path.join(turtlesim_plus_control_pkg,'viapoint','via_point_B.yaml')
        elif self.namespace == "/Iron":
            self.viapoint_path = os.path.join(turtlesim_plus_control_pkg,'viapoint','via_point_O.yaml')
        elif self.namespace == "/Melodic":
            pass

        # Create Class Variables
        self.counter = 0

        # Load positions from YAML file
        with open(self.viapoint_path) as file:
            positions = yaml.load(file, Loader=yaml.FullLoader)

        # Extract position from YAML file
        self.via_point = positions['via_point']

    # Services =======================================
    # Service Server Callback
    def arrived_notification_callback(self, req, res):
        if self.counter < len(self.via_point):
            self.set_goal_point(self.via_point[self.counter])
            self.counter = self.counter + 1
        else:
            self.finish_alphabet_notify()
        return Empty.Response()

    # Service Client Request
    def set_goal_point(self, position)->None:
        Target = SetTarget.Request()
        Target.target.x = position[0]
        Target.target.y = position[1]
        self.set_goal_client.call_async(Target)

    def finish_alphabet_notify(self):
        req = Empty.Request()
        self.finish_alphabet_notification_client.call_async(req)

    def finish_callback(self, msg):
        if msg.data:
            sleep(5)
            self.set_goal_point([10.7,10.7])

def main(args=None):
    rclpy.init(args=args)
    node = scheduler()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()