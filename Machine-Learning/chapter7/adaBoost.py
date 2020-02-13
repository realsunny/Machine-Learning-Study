import numpy as np
from buildStump import *


def adaBoost(train_data, label, w, num=40):  # 默认迭代次数40
    trees = []
    aggEstArr = np.zeros(5)  # 累计最终预测结果
    agg_est = np.zeros(5)
    for i in range(num):
        single_tree, minErr, estArr = buildStump(train_data, label, w)
        alpha = 1/2*(np.log((1-minErr)/max(minErr, 1e-16)))
        single_tree['alpha'] = alpha
        trees.append(single_tree)
        # 更新数据权重d
        expon = -alpha * estArr * label  # 预测正确则同号得1，预测错误则异号得-1
        w = w * np.exp(expon)
        w = w / sum(w)
        # 计算累计预测结果
        agg_est += alpha * estArr
        aggEstArr[np.sign(agg_est) != label] = 1
        errorRate = sum(aggEstArr) / len(train_data)
        aggEstArr = np.zeros(5)
        if errorRate == 0:
            print("the error rate is already 0")
            break
    return trees


if __name__ == "__main__":
    weight = np.ones(5) / 5
    train_data, label = load_data()
    trees = adaBoost(train_data, label, weight)
    print(trees)
