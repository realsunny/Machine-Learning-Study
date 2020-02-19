from numpy import *
import matplotlib.pyplot as plt

def loadData(filename):
    data = []
    f = open(filename)
    for line in f.readlines():
        temp = line.strip().split()
        xx = map(float, temp)
        data.append(list(map(float, temp)))
    return array(data)

def distance(vecA, vecB):
    return sqrt(sum((vecA - vecB)**2))


def draw(dataSet, clusterAssign, cents, k):
    k_cluster = []
    for i in range(k):
        k_cluster.append(dataSet[nonzero(clusterAssign[:, 0] == i)[0], :])
    # ***作散点图
    market = ['o', '>', '<', 'v']
    for j in range(k):
        plt.scatter(k_cluster[j][:, 0], k_cluster[j][:, 1], marker=market[j])
        plt.scatter(cents[j][0], cents[j][1], s=70, marker='+')
    plt.show()
    # ***

