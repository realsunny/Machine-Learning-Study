import numpy as np
from math import *


def load_train_data():
    train_data_matrix = []
    label_matrix = []
    with open("testSet.txt")as f:
        for line in f.readlines():
            temp = line.strip().split()
            train_data_matrix.append([1, float(temp[0]), float(temp[1])])
            label_matrix.append(int(temp[2]))
    return train_data_matrix, np.mat(label_matrix)


def load_horse_data(file_name):
    # 21个特征， 1个类标签
    data = []
    label = []
    f = open(file_name)
    for line in f.readlines():
        line_data = line.strip().split()
        line_arr = []
        for i in range(21):
            line_arr.append(float(line_data[i]))
        data.append(line_arr)
        label.append(int(float(line_data[21])))  # 不能直接将浮点数字符串转为int, 应先转float,再转int
    return data, label


def sigmoid(x):
    return 1.0/(1 + np.exp(-x))


def gradDesc(train_data, label):
    alpha = 0.001  # 定义梯度下降步长为0.01
    label_matrix = np.mat(label).transpose()
    train_matrix = np.mat(train_data).transpose()
    w = np.ones((len(train_data[0]), 1))  # 初始w值为（1，1，1）
    for i in range(500):
        h = sigmoid(np.dot(train_data, w))  # 100*1矩阵
        error = h - label_matrix
        w -= alpha * np.dot(train_matrix, error)  # 3*100 矩阵乘以100*1 矩阵

    return w


def improve_gradGradAscent(train_data, label, numTrain = 150):
    train_data = np.array(train_data)
    m, n = np.shape(train_data)  # m个样本,每个样本n个特征
    w = np.ones(n)
    for i in range(numTrain):
        data_index = list(range(m))
        for j in range(m):
            alpha = 4/(1.0 + i + j) + 0.01  # 更新步长
            rand_index = np.random.randint(0, len(data_index))
            mid = train_data[data_index[rand_index]]
            h = sigmoid(sum(mid * w))  #
            error = label[data_index[rand_index]] - h
            w = w + alpha * error * train_data[data_index[rand_index]]
            del(data_index[rand_index])
    return w


def classify(test_data, weight):
    # test_data是单个数据
    if sigmoid(sum(test_data * weight)) > 0.5:
        return 1
    else:
        return 0


if __name__ == "__main__":
    horse_train_data, horse_label = load_horse_data("horseColicTraining.txt")
    test_data, test_label = load_horse_data("horseColicTest.txt")
    test_data = np.array(test_data)
    for i in range(10):  # 计算十次
        w = improve_gradGradAscent(horse_train_data, horse_label)  # 每次的w都不同，因为存在随机
        correct = 0.0
        for i in range(len(test_data)):
            if classify(test_data[i], w) == test_label[i]:
                correct += 1
            else:
                pass
        print("the correct rate of the given test_set is %f" % (correct/len(test_data)))







