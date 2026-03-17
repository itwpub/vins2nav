# VINS2Nav (ROS 2 Jazzy)

本仓库提供一个**基于 OAK 4Dpro + VINS-Fusion + Nav2 + SLAM** 的视觉导航与建图系统参考实现，重点覆盖：

- 硬件接入与通信配置
- ROS 2 Jazzy 驱动与数据发布规范
- VINS-Fusion 视觉里程计集成
- Nav2 导航与定位接口配置
- 建图（2D/3D 可扩展）
- 联调、测试与文档化

## 目录结构

- `docs/system_design.md`：系统架构、数据流、模块接口与故障处理
- `docs/installation_guide.md`：安装部署、参数配置与运行步骤
- `docs/test_plan_and_report.md`：测试方案（功能/性能/稳定性）及报告模板
- `configs/vins_fusion_oak4dpro.yaml`：VINS-Fusion 对 OAK 4Dpro 的示例参数
- `configs/nav2_params.yaml`：Nav2 关键参数示例
- `configs/slam_toolbox_params.yaml`：SLAM Toolbox 建图参数示例
- `launch/bringup_vision_nav.launch.py`：统一启动文件（驱动+VINS+SLAM+Nav2）
- `scripts/check_topics.sh`：联调阶段的 Topic/TF 快速检查脚本

## 快速开始

1. 先阅读 `docs/installation_guide.md` 完成环境与依赖安装。
2. 根据机器人实际硬件修改 `configs/` 参数。
3. 使用 `launch/bringup_vision_nav.launch.py` 启动全链路。
4. 按 `docs/test_plan_and_report.md` 执行测试并记录结果。

> 说明：本仓库提供的是工程落地模板与参数化参考，实际部署时请结合机器人底盘、传感器外参与现场环境进行二次标定。
