from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time')
    nav2_params = LaunchConfiguration('nav2_params')
    slam_params = LaunchConfiguration('slam_params')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false'),
        DeclareLaunchArgument('nav2_params', default_value='configs/nav2_params.yaml'),
        DeclareLaunchArgument('slam_params', default_value='configs/slam_toolbox_params.yaml'),

        # OAK 4Dpro 驱动（示例，可替换为 depthai 官方 launch）
        Node(
            package='depthai_ros_driver',
            executable='camera_node',
            name='oak_camera',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
        ),

        # VINS-Fusion 节点（示例，按实际包名调整）
        Node(
            package='vins',
            executable='vins_node',
            name='vins_node',
            output='screen',
            parameters=['configs/vins_fusion_oak4dpro.yaml', {'use_sim_time': use_sim_time}],
        ),

        # 深度转激光（供 2D Nav2 使用）
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depth_to_scan',
            remappings=[
                ('depth', '/oak/stereo/depth'),
                ('scan', '/scan'),
            ],
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
        ),

        # SLAM Toolbox
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[slam_params],
        ),

        # Nav2 map_server（若纯 SLAM 模式可按需关闭）
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            output='screen',
            parameters=[nav2_params],
        ),

        Node(
            package='nav2_planner',
            executable='planner_server',
            name='planner_server',
            output='screen',
            parameters=[nav2_params],
        ),
        Node(
            package='nav2_controller',
            executable='controller_server',
            name='controller_server',
            output='screen',
            parameters=[nav2_params],
        ),
        Node(
            package='nav2_bt_navigator',
            executable='bt_navigator',
            name='bt_navigator',
            output='screen',
            parameters=[nav2_params],
        ),
        Node(
            package='nav2_behaviors',
            executable='behavior_server',
            name='behavior_server',
            output='screen',
            parameters=[nav2_params],
        ),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_navigation',
            output='screen',
            parameters=[{
                'use_sim_time': use_sim_time,
                'autostart': True,
                'node_names': [
                    'map_server',
                    'planner_server',
                    'controller_server',
                    'bt_navigator',
                    'behavior_server'
                ]
            }],
        ),
    ])
