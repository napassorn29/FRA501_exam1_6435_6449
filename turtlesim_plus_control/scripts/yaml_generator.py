#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import yaml, os
import math
import numpy as np
from ament_index_python.packages import get_package_share_directory

class YamlGenerator(Node):
    def __init__(self):
        super().__init__('yaml_generator')
        # path of file viapoint.yaml 
        my_pkg = get_package_share_directory('turtlesim_plus_control')
        self.yaml_file_path_F = os.path.join(my_pkg,'viapoint','via_point_F.yaml') # Set your desired YAML file path
        self.yaml_file_path_I = os.path.join(my_pkg,'viapoint','via_point_I.yaml')
        self.yaml_file_path_B = os.path.join(my_pkg,'viapoint','via_point_B.yaml')
        self.yaml_file_path_O = os.path.join(my_pkg,'viapoint','via_point_O.yaml')

    # generator path F,I,B,O (use angle(sin,cos) that the turtle will go and multiply it by the distance.)
    def generate_path(self):
        # config angle of path F,I,B,O
        degree = [[(math.pi/2),(math.pi/2),0,-(math.pi)/2,(math.pi)],
                  [(math.pi/2),(math.pi/2)],
                  [(math.pi/2),(math.pi/2),-(math.pi/6),math.pi+(math.pi/6),-(math.pi/6),math.pi+(math.pi/6)],
                  [0,(math.pi/2),(math.pi/2),math.pi,(-(math.pi)/2),(-(math.pi)/2)]]
        start = [[3.0,6.5],[7.0,6.5],[3.0,1.5],[7.0,1.5]]
        x = 0
        y = 0
        x_p = 0
        y_p = 0
        m = 0
        path = []
        for m in range(len(start)):
            path_one = [[start[m][0],start[m][1]]]
            x = start[m][0]
            y = start[m][1]
            d = 0
            # Check the position of each corner letter.
            for d in range(len(degree[m])):
                x_n = x + float(np.cos(degree[m][d])*1.5)
                y_n = y + float(np.sin(degree[m][d])*1.5)
                pizza = math.floor(19/len(degree[m]))
                p = 0
                if m == 0 :
                    pizza = math.floor(19/(len(degree[m]))+0.5)
                if d == len(degree[m]) - 1:
                    pizza = pizza+1
                    if m == 0 :
                        pizza = pizza - 2
                # Divide the total path into 20 points according to the pizza.
                for p in range(pizza):
                    if m == 0 and d == 3:
                        x_p = x_n
                        y_p = y_n
                    else:
                        if (y) != (y_n) and (x) == (x_n):
                            y_p = float(y + float((y_n - y) / pizza) * (p + 1))
                            x_p = x_n
                        elif (x) != (x_n) and (y) == (y_n):
                            x_p = float(x + float((x_n - x) / pizza) * (p + 1))
                            y_p = y_n
                        elif (x) != (x_n) and (y) != (y_n):
                            y_p = float(y + float((y_n - y) / pizza) * (p + 1))
                            x_p = float(x + float((x_n - x) / pizza) * (p + 1))
                    path_one.append([x_p,y_p])
                x = x_n
                y = y_n

            # array of path
            path.append(path_one)
        self.data = path


    # push path and create file in yaml file of F,I,B,O
    def generate_and_push_data(self):
        data_F = self.data[0]
        data_F = {'via_point': data_F}

        data_I = self.data[1]
        data_I = {'via_point': data_I}

        data_B = self.data[2]
        data_B = {'via_point': data_B}

        data_O = self.data[3]
        data_O = {'via_point': data_O}

        with open(self.yaml_file_path_F, 'w') as yaml_file:
            yaml.dump(data_F, yaml_file, default_flow_style=False)
            self.get_logger().info(f'Data written to {self.yaml_file_path_F}')
        
        with open(self.yaml_file_path_I, 'w') as yaml_file:
            yaml.dump(data_I, yaml_file, default_flow_style=False)
            self.get_logger().info(f'Data written to {self.yaml_file_path_I}')
        
        with open(self.yaml_file_path_B, 'w') as yaml_file:
            yaml.dump(data_B, yaml_file, default_flow_style=False)
            self.get_logger().info(f'Data written to {self.yaml_file_path_B}')
        
        with open(self.yaml_file_path_O, 'w') as yaml_file:
            yaml.dump(data_O, yaml_file, default_flow_style=False)
            self.get_logger().info(f'Data written to {self.yaml_file_path_O}')

def main(args=None):
    rclpy.init(args=args)
    node = YamlGenerator()
    node.generate_path()
    node.generate_and_push_data()
    rclpy.shutdown()

if __name__ == '__main__':
    main()