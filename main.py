import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
from matplotlib.animation import FuncAnimation
import random

# 黑色暗调画布，还原视频氛围感
fig, ax = plt.subplots(figsize=(10, 10), facecolor="#000000")
ax.set_xlim(-400, 400)
ax.set_ylim(-400, 400)
ax.set_aspect("equal")
ax.axis("off")

# 初始化流动烟雾粒子
smoke_list = []
for _ in range(160):
    smoke_list.append({
        "x": random.uniform(-390, 390),
        "y": random.uniform(-370, -100),
        "size": random.uniform(10, 70),
        "alpha": random.uniform(0.05, 0.23),
        "vx": random.uniform(-0.75, 0.75),
        "vy": random.uniform(-0.4, 0.1)
    })

# 贝塞尔曲线生成柔滑花瓣轮廓，模拟水晶曲面
def build_petal_path(center_x, center_y, rotate_angle, bloom_scale):
    rad = np.radians(rotate_angle)
    base_r = 175 * bloom_scale
    verts = [
        (center_x, center_y),
        (center_x + base_r * np.cos(rad - 0.4), center_y + base_r * np.sin(rad - 0.4)),
        (center_x + base_r * 1.4 * np.cos(rad), center_y + base_r * 1.4 * np.sin(rad)),
        (center_x + base_r * np.cos(rad + 0.4), center_y + base_r * np.sin(rad + 0.4)),
        (center_x, center_y)
    ]
    curve_codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4, Path.CLOSEPOLY]
    return Path(verts, curve_codes)

# 渲染完整花朵与烟雾
def render_flower(scale):
    ax.clear()
    ax.set_facecolor("#000000")
    ax.set_xlim(-400, 400)
    ax.set_ylim(-400, 400)
    ax.axis("off")

    # 更新流动烟雾
    for particle in smoke_list:
        particle["x"] += particle["vx"]
        particle["y"] += particle["vy"]
        # 烟雾循环重置，避免飘出画面
        if particle["y"] < -400:
            particle["y"] = random.uniform(-350, -100)
            particle["x"] = random.uniform(-390, 390)
        smoke_circle = plt.Circle((particle["x"], particle["y"]), particle["size"], color="#80bbff", alpha=particle["alpha"])
        ax.add_patch(smoke_circle)

    # 外层大花瓣
    outer_petal_num = 14
    for i in range(outer_petal_num):
        petal_path = build_petal_path(0, 0, i * 360 / outer_petal_num, scale)
        # 半透明水晶填充
        fill_patch = PathPatch(petal_path, facecolor="#d0e8ff", edgecolor="#ffffff", linewidth=2, alpha=0.3)
        # 花瓣边缘银色高光描边，还原视频金属亮边
        highlight_line = PathPatch(petal_path, fill=False, edgecolor="#f8fbff", linewidth=0.8, alpha=0.8)
        ax.add_patch(fill_patch)
        ax.add_patch(highlight_line)

    # 内层小花瓣
    inner_petal_num = 9
    for i in range(inner_petal_num):
        petal_path = build_petal_path(0, 0, i * 360 / inner_petal_num, scale * 0.63)
        inner_fill = PathPatch(petal_path, facecolor="#e4f1ff", edgecolor="#ffffff", linewidth=1.2, alpha=0.43)
        ax.add_patch(inner_fill)

    # 花蕊透光中心
    core = plt.Circle((0, 0), 23 * scale, color="#f6fbff", alpha=0.7)
    ax.add_patch(core)
    # 通透蓝色花茎
    ax.plot([0, 0], [-175 * scale, -400], color="#5090dd", linewidth=6, alpha=0.35)
    return ax

# 动画逐帧更新逻辑，实现缓慢绽放
def update_frame(frame_idx):
    bloom_ratio = frame_idx / 55
    render_flower(bloom_ratio)
    return ax,

# 生成绽放动画
animation = FuncAnimation(fig, update_frame, frames=58, interval=48, blit=False)
plt.show()