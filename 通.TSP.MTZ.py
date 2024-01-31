import numpy as np
import pandas as pd
from gurobipy import *
from math import cos, sin, acos, pi

# 定义弧度转换函数
def to_radians(coord):
    return coord * pi / 180

# 简化球面距离计算函数
def haversine_distance(i_index, j_index):
    x1, y1 = data_df.loc[i_index, ['longitude', 'latitude']].values * pi / 180
    x2, y2 = data_df.loc[j_index, ['longitude', 'latitude']].values * pi / 180
    outcom = sin(x1 - x2) * sin(x1 - x2) * cos(y1) * cos(y2) + sin((y1 - y2)/2) * sin((y1 - y2)/2)
    return round(6370 * acos(outcom), 4)

if __name__ == "__main__":
    # 导入数据并建立距离矩阵
    data_df = pd.read_csv(r"TSP_Data.txt")
    N = len(data_df)

    # 创建全零距离矩阵，并填充实际距离（包含虚拟节点）
    dis_mtx = np.zeros((N+1, N+1))
    for i in range(N):
        dis_mtx[i, N] = haversine_distance(i, 0)
        dis_mtx[N, i] = dis_mtx[i, N]
        for j in range(i+1):  # 可以避免重复计算对称项
            dis_mtx[i, j] = dis_mtx[j, i] = haversine_distance(i, j)

    # 创建集合索引并构建index_tplst
    index_tplst = [(i, j) for i in range(N) for j in range(i+1, N+1)]

    # 建立优化模型
    m = Model()
    m.setParam(GRB.Param.MIPGap, 0.01)

    # 添加变量
    x = m.addVars(index_tplst, vtype=GRB.BINARY, name='x')
    u = m.addVars(range(N+1), lb=0.0, vtype=GRB.CONTINUOUS, name='u')

    # 设置目标函数
    m.setObjective(sum(dis_mtx[i, j] * x[i, j] for i, j in index_tplst))

    # 添加约束条件
    m.addConstrs(sum(x[i, j] for i, j in index_tplst if j == k) == 1 for k in range(1, N+1))  # 流入约束
    m.addConstrs(sum(x[i, j] for i, j in index_tplst if i == k) == 1 for k in range(N))     # 流出约束
    m.addConstrs(u[i] - u[j] + N * x[i, j] <= N - 1 for i, j in index_tplst)               # MTZ约束

    # 保存LP文件
    m.write('TSP_MTZ.lp')

    # 求解
    m.optimize()

    # 输出结果
    print("____________求解结果____________")
    for var in m.getVars():
        if var.X != 0:
            print(f"{var.VarName}: {var.X}")
    print("目标函数值:", m.ObjVal)