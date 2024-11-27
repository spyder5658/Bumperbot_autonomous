from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument,OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition

def noisy_controller(context,*args,**kwargs):
    wheel_radius = float(LaunchConfiguration("wheel_radius").perform(context))
    wheel_separation = float(LaunchConfiguration("wheel_separation").perform(context))
    wheel_radius_error = float(LaunchConfiguration("wheel_radius_error").perform(context))
    wheel_separation_error = float(LaunchConfiguration("wheel_separation_error").perform(context))

    noisy_controller_py=Node(
        package="bumperbot_controller",
        executable="noisy_controller.py",
        parameters=[
            {"wheel_radius":wheel_radius+wheel_radius_error,
             "wheel_separation":wheel_separation+wheel_separation_error}
        ]
    )
    return [noisy_controller_py]



def generate_launch_description():

    use_python_arg = DeclareLaunchArgument(
        name="use_python",
        default_value="True"
    )
    wheel_radius_arg = DeclareLaunchArgument(
        name="wheel_radius",
        default_value="0.033"
    )

    wheel_separation_arg = DeclareLaunchArgument(
        name="wheel_separation",
        default_value="0.17"
    )
    wheel_radius_error_arg = DeclareLaunchArgument(
        name="wheel_radius_error",
        default_value="0.005"
    )

    wheel_separation_error_arg = DeclareLaunchArgument(
        name="wheel_separation_error",
        default_value="0.02"
    )


    use_python =LaunchConfiguration("use_python")
    #LuanchConfiguration reads the runtime value of the arguments declared
    wheel_radius = LaunchConfiguration("wheel_radius")
    wheel_separation = LaunchConfiguration("wheel_separation")





    joint_state_broadcaster_spawner=Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager"
        ]
    )

    simple_controller=Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "simple_velocity_controller",
            "--controller-manager",
            "/controller_manager"
        ]
    )

    simple_controller_py=Node(
        package="bumperbot_controller",
        executable="simple_controller.py",
        parameters=[{"wheel_radius":wheel_radius,
                     "wheel_separation":wheel_separation}],
        condition=IfCondition(use_python)
    )

    noisy_controller_launch = OpaqueFunction(function=noisy_controller)


    return LaunchDescription([
        use_python_arg,
        wheel_radius_error_arg,
        wheel_separation_error_arg,
        wheel_radius_arg,
        wheel_separation_arg,
        joint_state_broadcaster_spawner,
        simple_controller,
        simple_controller_py,
        noisy_controller_launch

    ])