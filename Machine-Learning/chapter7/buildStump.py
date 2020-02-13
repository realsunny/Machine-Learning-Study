import numpy as np


def load_data():
    # 仅直接初始化几个简单数据
    train_data = np.array([[1, 2.1],
                           [2, 1.1],
                           [1.3, 1],
                           [1, 1],
                           [2, 1]])
    label = np.array([1, 1, -1, -1, 1])
    return train_data, label  # 数据格式为 train_data:5*2 , label为:1*5


def stumpClassify(train_data, inequal, dim, threshVal):
    predictArr = np.ones(np.shape(train_data)[0])
    if inequal == 'lt':
        predictArr[train_data[:, dim] <= threshVal] = -1  # 在阈值线左边的被分为-1类
    else:
        predictArr[train_data[:, dim] > threshVal] = -1  # 在阈值线右边的被分为-1类
    return predictArr


# 核心函数，构建单层决策树
def buildStump(train_data, label, w):
    m, n = np.shape(train_data)
    numSteps = 10
    min_wError = float('inf')
    best_stump = {}
    best_pre_arr = np.ones(m)
    for dim in range(n):  # 第i维特征
        maxVal = np.max(train_data[:, dim])
        minVal = np.min(train_data[:, dim])
        stepSize = (maxVal - minVal) / numSteps
        for j in range(-1, numSteps + 1):  # 阈值从左边界 到 右边界，11次循环
            threshVal = minVal + j * stepSize
            for inequal in ['lt', 'gt']:
                error_arr = np.ones(m)
                predictArr = stumpClassify(train_data, inequal, dim, threshVal)  # 得到算法分类的结果数组
                error_arr[predictArr == label] = 0  # 比较array中每个元素， 若相同则置0
                w_error = sum(error_arr * w)
                print("spilt, dim:%d, threshVal:%.3f, inequal:%s, weight error:%.3f" % (dim, threshVal, inequal,
                                                                                        w_error))
                if w_error < min_wError:
                    best_pre_arr = predictArr.copy()
                    min_wError = w_error
                    best_stump['dim'] = dim
                    best_stump['threshVal'] = threshVal
                    best_stump['inequal'] = inequal
    print("the best stump is :", best_stump)
    print("the min weight error is ", min_wError)
    print("the best predict is ", best_pre_arr)
    return best_stump, min_wError, best_pre_arr


if __name__ == "__main__":
    # w是数据权重，可以人为自定
    w = np.array([0.28571429, 0.07142857, 0.07142857, 0.07142857, 0.5])  # 给5个样本，每个样本2个特征
    train_data, label = load_data()
    buildStump(train_data, label, w)
