from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import GroupAction, DeclareLaunchArgument, ExecuteProcess, RegisterEventHandler
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    x_launch_arg = DeclareLaunchArgument('x', default_value='0.5')
    y_launch_arg = DeclareLaunchArgument('y', default_value='0.5')

    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    
    namespace_F = 'Foxy'
    namespace_I = 'Noetic'
    namespace_B = 'Humble'
    namespace_O = 'Iron'
    
    my_pkg_config = get_package_share_directory('turtlesim_plus_control')
    file_config_f = os.path.join(my_pkg_config,'config','F_controller_config.yaml')
    file_config_i = os.path.join(my_pkg_config,'config','I_controller_config.yaml')
    file_config_b = os.path.join(my_pkg_config,'config','B_controller_config.yaml')
    file_config_o = os.path.join(my_pkg_config,'config','O_controller_config.yaml')

    kill_turtle1 = ExecuteProcess(
        cmd = [["ros2 service call /remove_turtle turtlesim/srv/Kill 'name: turtle1'"]],
        shell=True
    )

    spawn_turtle_F = ExecuteProcess(
        cmd = [['ros2 service call /spawn_turtle turtlesim/srv/Spawn "{x: ',x,', y: ',y,', theta: 0.0, name: \'',namespace_F,'\'}"']]
        ,shell = True
    )
    spawn_turtle_I = ExecuteProcess(
        cmd = [['ros2 service call /spawn_turtle turtlesim/srv/Spawn "{x: ',x,', y: ',y,', theta: 0.0, name: \'',namespace_I,'\'}"']]
        ,shell = True
    )
    spawn_turtle_B = ExecuteProcess(
        cmd = [['ros2 service call /spawn_turtle turtlesim/srv/Spawn "{x: ',x,', y: ',y,', theta: 0.0, name: \'',namespace_B,'\'}"']]
        ,shell = True
    )
    spawn_turtle_O = ExecuteProcess(
        cmd = [['ros2 service call /spawn_turtle turtlesim/srv/Spawn "{x: ',x,', y: ',y,', theta: 0.0, name: \'',namespace_O,'\'}"']]
        ,shell = True
    )

    turtlesim = Node(
        package='turtlesim_plus',
        executable='turtlesim_plus_node.py'
    )

    gen_path = Node(
        package='turtlesim_plus_control',
        executable='yaml_generator.py'
    )

    observer = Node(
        package='turtlesim_plus_control',
        executable='observer.py'
    )

    scheduler_action = GroupAction(
        actions=[
            Node(
                package='turtlesim_plus_control',
                executable='scheduler.py',
                namespace=namespace_F
            ),
            Node(
                package='turtlesim_plus_control',
                executable='scheduler.py',
                namespace=namespace_I
            ),
            Node(
                package='turtlesim_plus_control',
                executable='scheduler.py',
                namespace=namespace_B
            ),
            Node(
                package='turtlesim_plus_control',
                executable='scheduler.py',
                namespace=namespace_O
            )
        ]
    )

    controller_action = GroupAction(
        actions=[
            Node(
                package='turtlesim_plus_control',
                executable='controller.py',
                namespace=namespace_F,
                parameters=[file_config_f]
            ),
            Node(
                package='turtlesim_plus_control',
                executable='controller.py',
                namespace=namespace_I,
                parameters=[file_config_i]
            ),
            Node(
                package='turtlesim_plus_control',
                executable='controller.py',
                namespace=namespace_B,
                parameters=[file_config_b]
            ),
            Node(
                package='turtlesim_plus_control',
                executable='controller.py',
                namespace=namespace_O,
                parameters=[file_config_o]
            )
        ]
    )

    launch_description = LaunchDescription()

    launch_description.add_action(gen_path)
    launch_description.add_action(turtlesim)
    launch_description.add_action(x_launch_arg)
    launch_description.add_action(y_launch_arg)
    launch_description.add_action(kill_turtle1)
    launch_description.add_action(spawn_turtle_F)
    launch_description.add_action(spawn_turtle_I)
    launch_description.add_action(spawn_turtle_B)
    launch_description.add_action(spawn_turtle_O)
    launch_description.add_action(observer)
    launch_description.add_action(scheduler_action)
    launch_description.add_action(controller_action)

    return launch_description