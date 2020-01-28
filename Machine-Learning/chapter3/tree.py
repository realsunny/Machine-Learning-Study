from math import *
def initdata():
    a = []
    dataset = []
    with open("training-data")as f:
        for line in f.readlines():
            temp = line.strip().split()
            a = [int(temp[0]), int(temp[1]), temp[2]]
            dataset.append(a)
    return dataset


def calcShannon(dataset):
    shannondic = {}
    numOfdata = len(dataset)
    for data in dataset:
        label = data[-1]
        shannondic[label] = shannondic.get(label, 0) + 1
    shannonEntropy = 0.0
    for key in shannondic:
        prob = shannondic[key]/numOfdata
        shannonEntropy -= prob*log(prob, 2)
    return shannonEntropy


def spiltDataset(dataset, axis, value):
    """
    过滤出dataset数据集中第axis个（0开始计数）特征值=value 的值
    :param dataset: 待划分数据集
    :param axis: 第几个特征
    :param value:
    :return:
    """
    restDataset = []
    for data in dataset:
        if data[axis] == value:
            temp = data[:axis]
            temp.extend(data[axis+1:])
            restDataset.append(temp)
    return restDataset


def chooseBestFea(dataset):
    """
    给定数据集dataset,返回最好划分的特征的索引序号（0开始计数）
    :param dataset:
    :return:
    """
    numFea = len(dataset[0])-1 #特征数
    bestFea = -1
    bestShannonEnt = calcShannon(dataset)#原始数据集的熵
    for i in range(numFea):
        newShannonEnt = 0
        feaValueList = set([fea[i] for fea in dataset])#第i个特征的所有不重复取值
        for value in feaValueList:
            subdataset = spiltDataset(dataset, i, value)
            prob = len(subdataset)/len(dataset)
            newShannonEnt += prob*calcShannon(subdataset)
        if newShannonEnt < bestShannonEnt:
            bestShannonEnt = newShannonEnt
            bestFea = i
    return bestFea


def majority(classList):
    classdic = {}
    for a in classList:
        classdic[a] = classdic.get(classdic[a], 0)+1
    sortedClassdic = sorted(classdic.items(), key=lambda x: x[1], reverse=True)
    return sortedClassdic[0][0]


def createTree(dataset, labels):
    classList = [example[-1] for example in dataset]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataset[0]) == 1:
        return majority(classList)
    bestFeature = chooseBestFea(dataset)
    bestFeatureLabel = labels[bestFeature]
    myTree = {bestFeatureLabel: {}}
    del(labels[bestFeature])
    feaValues = set([example[bestFeature] for example in dataset])#所有不重复特征的值
    for value in feaValues:
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree(spiltDataset(dataset, bestFeature, value), subLabels)
    return myTree


def classify(tree, fea_labels, test_data):
    firstStr = list(tree.keys())[0]
    index = fea_labels.index(firstStr)
    secondDic = tree[firstStr]
    for key in secondDic.keys():
        if test_data[index] == key:
            if type(secondDic[key]).__name__ == 'dict':
                classLabel = classify(secondDic[key], fea_labels, test_data)
            else:
                classLabel = secondDic[key]
    return classLabel


if __name__ =="__main__":
    labels = ['no surfacing', 'flippers']
    feaLabels = labels[:]
    dataset = initdata() #从文件中读数据
    mytree = createTree(dataset, labels)
    print(mytree)
    print(classify(mytree, feaLabels, [1, 1]))