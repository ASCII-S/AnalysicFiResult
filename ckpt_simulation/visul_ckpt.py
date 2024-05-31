import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 数据点
x = np.array([1, 2, 3])
y = np.array([1, 2, 3])
X, Y = np.meshgrid(x, y)
Z = np.array([[10, 20, 30],
              [15, 25, 35],
              [20, 30, 40]])  # 第三个维度

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 绘制曲面图
ax.plot_surface(X, Y, Z)

# 设置坐标轴标签
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.savefig('visual_ckpt.png')
