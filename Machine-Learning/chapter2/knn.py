import numpy as np
from math import *
def data_init(filename):
    data = []
    with open(filename)as f:
        for line in f.readlines():
            data.append(line.strip())
    return np.loadtxt(filename)

def caculate(data1, data2):
    """
    计算两个点的距离
    :param data1:
    :param data2:
    :return:
    """
    return sqrt((data1[0]-data2[0])**2 + (data1[1]-data2[1])**2)

def knn(train_data, test_data, k):
    distance = []
    for tra_data in train_data:
        distance.append((caculate(test_data, tra_data), tra_data[2]))
    print("排序前距离")
    print(distance)
    distance.sort()
    print("排序后距离")
    print(distance)
    #对前k个距离最小的样本，找出类别最多出现的作为最终结果
    ans = {}
    for i in range(k):
        ans[distance[i][1]] = ans.get(distance[i][1], 0)+1
    print("字典排序前")
    for item in ans.items():
        print(item)
    print("字典排序后")
    print(sorted(ans.items(), key=lambda x:x[1], reverse=True))
    return sorted(ans.items(), key=lambda x:x[1], reverse=True)[0][0]#字典排序后变列表

def main():
    train_data = data_init('training-data')
    test_data = data_init('test-data')
    print(knn(train_data, test_data, 5))

if __name__=="__main__":
    main()