from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    ld = LaunchDescription()

    ir_data=Node(
        package="sensor_data",
        executable="infrared_data"
    )
    us_data=Node(
        package="sensor_data",
        executable="ultrasonic_data"
    )
    controller=Node(
        package="sensor_data",
        executable="line_controller"
    )

    ld.add_action(ir_data)
    ld.add_action(us_data)
    ld.add_action(controller)

    return ld