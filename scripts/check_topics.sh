#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] 检查关键 topic 是否存在"
ros2 topic list | rg -E "/oak/left/image_raw|/oak/right/image_raw|/oak/stereo/depth|/oak/imu|/odometry/vins|/scan|/map" || true

echo "[2/4] 检查图像频率"
ros2 topic hz /oak/left/image_raw --window 30 || true

echo "[3/4] 检查里程计频率"
ros2 topic hz /odometry/vins --window 30 || true

echo "[4/4] 检查 TF 连通"
ros2 run tf2_ros tf2_echo map base_link || true
