#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool

class observer(Node):
    def __init__(self):
        super().__init__('observer')
        self.create_subscription(Bool, 'Foxy/finished_alphabet', self.F_finished_alphabet_callback, 10)
        self.create_subscription(Bool, 'Noetic/finished_alphabet', self.I_finished_alphabet_callback, 10)
        self.create_subscription(Bool, 'Humble/finished_alphabet', self.B_finished_alphabet_callback, 10)
        self.create_subscription(Bool, 'Iron/finished_alphabet', self.O_finished_alphabet_callback, 10)
        self.create_timer(0.01, self.timer_callback)
        self.pub_finished = self.create_publisher(Bool,'/finished', 10)

        self.f_fin = 0
        self.i_fin = 0
        self.b_fin = 0
        self.o_fin = 0
        self.total_fin = 0
    
    def timer_callback(self):
        self.finish_pub()

    def F_finished_alphabet_callback(self, msg):
        if msg.data:
            self.f_fin = 1
        else:
            self.f_fin = 0

    def I_finished_alphabet_callback(self, msg):
        if msg.data:
            self.i_fin = 1
        else:
            self.i_fin = 0

    def B_finished_alphabet_callback(self, msg):
        if msg.data:
            self.b_fin = 1
        else:
            self.b_fin = 0

    def O_finished_alphabet_callback(self, msg):
        if msg.data:
            self.o_fin = 1
        else:
            self.o_fin = 0

    def finish_pub(self):
        self.total_fin = self.f_fin + self.i_fin + self.b_fin + self.o_fin
        result = Bool()
        result.data = False
        if self.total_fin == 4:
            result.data = True
        self.pub_finished.publish(result)

def main(args=None):
    rclpy.init(args=args)
    node = observer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()