# 基于 Nav2 的视觉导航与建图系统设计文档

## 1. 目标与范围

本文档描述 ROS 2 Jazzy 环境下，使用 OAK 4Dpro 双目深度相机、VINS-Fusion 和 Nav2 实现视觉导航与建图系统的工程设计。

覆盖范围：

1. 硬件集成
2. 驱动开发/配置
3. VINS-Fusion 集成
4. Nav2 系统配置
5. 建图功能实现
6. 系统联调
7. 测试验证
8. 故障排除与运维建议

---

## 2. 总体架构

### 2.1 模块划分

- **传感器层**：OAK 4Dpro（双目图像 + 深度 + IMU）
- **感知与状态估计层**：
  - depthai_ros_driver（采集并发布标准 ROS2 消息）
  - VINS-Fusion（视觉惯性里程计，输出 `/odometry/vins`）
- **地图层**：SLAM Toolbox（2D 占据栅格）或 OctoMap（3D）
- **导航层**：Nav2（map_server / amcl or external localization / planner / controller / bt_navigator）
- **执行层**：底盘控制器（接收 `/cmd_vel`）

### 2.2 关键数据流

1. OAK 4Dpro 输出：
   - `/oak/left/image_raw`
   - `/oak/right/image_raw`
   - `/oak/stereo/depth`
   - `/oak/imu`
2. VINS-Fusion 订阅双目图像+IMU，发布：
   - `/odometry/vins` (`nav_msgs/Odometry`)
   - `/tf`（`odom -> base_link`）
3. SLAM 订阅深度/点云 + 里程计，发布：
   - `/map` (`nav_msgs/OccupancyGrid`)
   - `/tf`（`map -> odom`）
4. Nav2 使用 `/map`、`/tf`、激光替代输入（由深度转 LaserScan 或点云层代价地图）完成全局/局部规划并输出 `/cmd_vel`。

### 2.3 坐标系约定

- `map`：全局地图坐标
- `odom`：局部连续坐标
- `base_link`：机器人本体
- `oak_camera_frame`：相机主坐标

静态外参建议使用 `robot_state_publisher + static_transform_publisher` 管理。

---

## 3. 硬件集成设计

## 3.1 物理连接

- OAK 4Dpro 通过 USB 3.0 连接计算单元。
- 相机安装在机器人顶部前向，避免强震动与遮挡。
- 供电稳定（建议独立稳压供电，避免底盘大电流干扰）。

### 3.2 通信与带宽

- 图像分辨率建议从 `640x400@30fps` 起步，逐步提升。
- 初期联调关闭非必要流（如高频 RGB）以降低总线压力。

### 3.3 校准要求

- 双目内参/外参：使用厂家标定数据复核。
- IMU-相机时空对齐：确保时间戳统一（系统时钟/NTP/PTP）。
- 相机与 `base_link` 外参：手工测量 + 在线优化校正。

---

## 4. 驱动设计（ROS2 Jazzy）

### 4.1 推荐驱动栈

- 使用 `depthai_ros_driver` 作为 OAK 4Dpro 驱动基础。

### 4.2 标准消息规范

- 图像：`sensor_msgs/Image`
- 相机内参：`sensor_msgs/CameraInfo`
- 深度/点云：`sensor_msgs/Image`（depth）/`sensor_msgs/PointCloud2`
- IMU：`sensor_msgs/Imu`

### 4.3 QoS 建议

- 图像类：`best_effort + keep_last(5)`
- 里程计/控制：`reliable + keep_last(10)`
- TF：默认 TF QoS

---

## 5. VINS-Fusion 集成设计

### 5.1 接口定义

- 输入：
  - 左右目图像（已校正）
  - IMU 数据
- 输出：
  - `nav_msgs/Odometry` (`/odometry/vins`)
  - `geometry_msgs/PoseStamped`（可选）
  - TF `odom -> base_link`

### 5.2 关键参数

- 双目话题映射
- IMU 噪声参数
- 外参初始化方式（固定/在线估计）
- 回环检测开关（按算力启用）

### 5.3 时延控制

- 统一使用系统时钟并启用 `use_sim_time` 的可配置开关。
- 监控图像-IMU 对齐误差（目标 < 5ms）。

---

## 6. Nav2 配置设计

### 6.1 组件

- `map_server`
- `amcl`（可选，若完全依赖 VINS + SLAM 可替换）
- `planner_server`
- `controller_server`
- `bt_navigator`
- `behavior_server`
- `lifecycle_manager`

### 6.2 里程计融合策略

优先将 VINS 输出作为 `odom` 主来源；如有轮速计，可通过 robot_localization 融合，增强短时鲁棒性。

### 6.3 代价地图输入

- 深度转 LaserScan（depthimage_to_laserscan）用于 2D 成本地图
- 或 PointCloud2 直接进入 voxel layer

---

## 7. 建图功能实现

### 7.1 方案选择

- **2D 实时导航优先**：SLAM Toolbox（推荐）
- **3D 语义/体素扩展**：OctoMap（后续）

### 7.2 输入与输出

- 输入：深度/点云 + VINS 里程计
- 输出：`/map` + 保存地图（pgm/yaml 或 bt）

### 7.3 地图更新策略

- 初始建图阶段提高更新频率
- 运营阶段降低频率并启用地图持久化

---

## 8. 系统联调流程

1. 单独验证相机节点（图像/深度/IMU）
2. 验证 VINS 输出稳定性与漂移水平
3. 验证 SLAM 建图闭环完整性
4. 接入 Nav2 完成从定位到控制闭环
5. 场景化任务联调（多目标点、动态障碍）

---

## 9. 风险与故障排除

### 9.1 常见问题

- 图像卡顿：降低分辨率/帧率，检查 USB 带宽
- VINS 发散：检查外参与时间同步
- Nav2 抖动：优化局部规划器加速度约束与 costmap 参数
- 地图撕裂：检查 TF 树是否存在多源冲突

### 9.2 监控指标

- Topic 频率稳定性（目标：>95% 在阈值内）
- 端到端导航成功率
- 回环后全局误差收敛情况

