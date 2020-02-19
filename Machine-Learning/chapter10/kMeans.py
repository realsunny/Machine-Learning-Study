import numpy
from numpy import *

from publicFunc import *


def randCents(dataSet, k):
    n = shape(dataSet)[1]
    cents = zeros((k, n))  # 初始化k个质心
    for i in range(n):  # 对每个特征
        minVal = min(dataSet[:, i])
        maxVal = max(dataSet[:, i])
        rangeI = maxVal - minVal
        cents[:, i] = rangeI * numpy.random.rand(1, k)
    return cents


def kMeans(dataSet, k):
    m, n = shape(dataSet)
    cents = randCents(dataSet, k)
    isChange = True
    dataAssign = zeros((m, 2))  # （索引号， 误差）
    while isChange:  # 每次分配有变，则全部重新计算再分配
        isChange = False
        minIndex = -1  # 最短距离点的索引
        for i in range(m):  # 对每个点分配到一个簇
            # ------------------找到距离该点最近的质心
            minDist = inf
            for j in range(k):
                dist = distance(dataSet[i], cents[j])
                if dist < minDist:
                    minIndex = j
                    minDist = dist
            # --------------------------
            if dataAssign[i, 0] != minIndex:
                isChange = True
            dataAssign[i, :] = minIndex, minDist ** 2
        # 更新每个簇的质心
        if isChange:
            k_cluster = []  # 记录所有簇的点的信息
            for i in range(k):  # 对第i个质心
                k_cluster.append(dataSet[nonzero(dataAssign[:, 0] == i)[0]])
                # print("第%d个簇, 长度%d:" % (i, len(k_cluster[i])))
                # print(k_cluster[i])
                # print("*************")
                if len(k_cluster[i]) != 0:
                    cents[i, :] = mean(k_cluster[i], axis=0)  # 计算每一列的均值

    return cents, dataAssign


def bisectKmeans(dataSet, k):
    # 初始化
    m, n = shape(dataSet)
    clusterAssign = zeros((m, 2))
    centList = []
    cent0 = mean(dataSet, axis=0)
    centList.append(cent0)
    bestSplitIndex = -1
    bestSplitAssign = []
    bestSplitCents = []
    # 遍历每个簇，进行试分割并计算最小的分割sse
    while len(centList) < k:
        minSse = inf
        for i in range(len(centList)):  # 对每一个簇
            subDataSet = dataSet[nonzero(clusterAssign[:, 0] == i)[0], :]
            # print(len(subDataSet))
            if len(subDataSet) != 0:
                splitCent, splitAssign = kMeans(subDataSet, 2)
                splitedSse = sum(splitAssign[:, 1]) + sum(dataSet[nonzero(clusterAssign[:, 0] != i)[0], 1])
                if splitedSse < minSse:
                    minSse = splitedSse
                    bestSplitIndex = i
                    bestSplitAssign = splitAssign.copy()
                    bestSplitCents = splitCent
            else:
                continue

        # 正式切分
        bestSplitAssign[nonzero(bestSplitAssign[:, 0] == 1)[0], 0] = len(centList)  # 这俩顺序不能搞反
        bestSplitAssign[nonzero(bestSplitAssign[:, 0] == 0)[0], 0] = bestSplitIndex  # 新增的两个簇号一个用被切分的，一个用簇的个数
        clusterAssign[nonzero(clusterAssign[:, 0] == bestSplitIndex)[0], :] = bestSplitAssign
        centList[bestSplitIndex] = bestSplitCents[0, :]
        centList.append(bestSplitCents[1, :])
    #draw(dataSet, clusterAssign, centList, 3)
    return centList, clusterAssign, minSse


if __name__ == "__main__":
    data = loadData("testSet2.txt")
    ans_sse = inf
    ans_cent = []
    ans_assign = []
    for i in range(20):  # 运行函数20次，取误差最小的结果
        cents, assign, minSse = bisectKmeans(data, 3)
        print(minSse)
        if minSse < ans_sse:
            ans_sse = minSse
            ans_cent = cents
            ans_assign = assign
    print("the minsse:%f" % ans_sse)
    print("the ans_assign :", ans_assign)
    print("the ans_cent", ans_cent)
    draw(data, ans_assign, ans_cent, 3)
