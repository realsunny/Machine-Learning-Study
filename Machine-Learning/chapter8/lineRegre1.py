"""
梯度下降求线性回归
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def loadData():
    train_data = []
    goal_data = []
    f = open("ex0.txt")
    for line in f.readlines():
        temp = line.strip().split()
        train_data.append([float(temp[0]), float(temp[1])])
        goal_data.append(float(temp[2]))
    return np.array(train_data), np.array(goal_data)


def gradDesc(train_data, goal_data):
    """
    梯度下降求w
    :param train_data: 训练数据的x值
    :param goal_data: 训练数据的y值
    :return:
    """
    alpha = 0.001  # 步长
    numCycle = 1000  # 迭代次数
    m, n = np.shape(train_data)
    w = np.ones(n)
    for i in range(numCycle):
        predict = np.dot(w, np.transpose(train_data))
        error = predict - goal_data
        grad = np.dot(error, train_data)
        w = w - alpha * grad
    return w


if __name__ == '__main__':
    x_data, y_value = loadData()
    w = gradDesc(x_data, y_value)
    print(w)
    #x_data = np.sort(x_data, axis=0)  # 按照列排序
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_data[:, 1], y_value)

    x_copy = x_data.copy()
    y_pre = np.dot(w, np.transpose(x_data))
    ax.plot(x_copy[:, 1], y_pre)
    plt.show()