# 安装与配置指南（ROS 2 Jazzy）

## 1. 环境准备

- Ubuntu 24.04
- ROS 2 Jazzy
- 推荐 GPU/CPU：8 核 CPU + 16GB RAM 起步

```bash
sudo apt update
sudo apt install -y ros-jazzy-desktop python3-colcon-common-extensions git
```

## 2. 工作空间初始化

```bash
mkdir -p ~/vision_nav_ws/src
cd ~/vision_nav_ws/src
```

将本仓库拷贝到 `~/vision_nav_ws/src/vins2nav`。

## 3. 依赖安装

> 根据实际仓库与版本调整。

```bash
cd ~/vision_nav_ws
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```

建议额外安装：

```bash
sudo apt install -y \
  ros-jazzy-nav2-bringup \
  ros-jazzy-slam-toolbox \
  ros-jazzy-depthimage-to-laserscan \
  ros-jazzy-robot-localization
```

## 4. OAK 4Dpro 驱动接入

1. 安装 depthai ROS 驱动（源码或二进制）。
2. 通过 udev 规则固定设备权限。
3. 启动后确认以下 Topic 存在：
   - `/oak/left/image_raw`
   - `/oak/right/image_raw`
   - `/oak/stereo/depth`
   - `/oak/imu`

验证命令：

```bash
ros2 topic list | rg "oak|imu|depth"
ros2 topic hz /oak/left/image_raw
```

## 5. VINS-Fusion 配置

- 复制 `configs/vins_fusion_oak4dpro.yaml` 到 VINS 节点配置路径。
- 修改参数：
  - 相机 topic 名称
  - 相机内参与外参
  - IMU 噪声

验证：

```bash
ros2 topic echo /odometry/vins --once
ros2 run tf2_ros tf2_echo odom base_link
```

## 6. Nav2 与 SLAM 配置

- Nav2 参数参考：`configs/nav2_params.yaml`
- SLAM 参数参考：`configs/slam_toolbox_params.yaml`

编译并加载环境：

```bash
cd ~/vision_nav_ws
colcon build --symlink-install
source install/setup.bash
```

统一启动：

```bash
ros2 launch vins2nav bringup_vision_nav.launch.py
```

## 7. 联调建议

1. 先不开导航，仅跑传感器 + VINS + SLAM。
2. 地图稳定后再启动 Nav2。
3. 最后接入目标点与自动导航。

## 8. 故障排除

- 没有图像：检查 USB 与供电、查看 `dmesg`。
- 没有里程计：检查 VINS 输入 topic 与时间戳。
- 无法规划：检查 map/odom/base_link TF 连通性。

常用命令：

```bash
ros2 topic list
ros2 topic hz /odometry/vins
ros2 run tf2_tools view_frames
```

