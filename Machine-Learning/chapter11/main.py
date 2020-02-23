def loadData():
    dataSet = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    return list(map(frozenset, dataSet))  # map返回迭代器， 全部用List转换


def createC1(dataSet):
    C1 = []
    for dt in dataSet:
        for item in dt:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return list(map(frozenset, C1))  # set不能作为字典键，frozenset可以


def Filter(dataSet, Ck, minSup):  # 输入Ck, 过滤后返回Lk
    Lk = []
    supData = {}
    dic = {}
    numItems = len(dataSet)
    for dt in dataSet:
        for ck in Ck:
            if ck.issubset(dt):
                dic[ck] = dic.get(ck, 0) + 1
    for key in dic:
        sup = dic[key] / numItems
        if sup >= minSup:
            Lk.append(key)
        supData[key] = sup
    return Lk, supData

def aprigen(Lk):
    Ck = []
    l = len(Lk[0])
    if len(Lk) == 1:
        return Ck
    else:
        for i in range(len(Lk)):
            for j in range(i+1, len(Lk)):
                temp = Lk[i] | Lk[j]
                if len(temp) == l+1:
                    if not temp in Ck:
                        Ck.append(temp)
    return Ck

def calConf(ruleList, freqSet, H, supData, minConf):
    for midSet in H:
        conf = supData[freqSet] / supData[midSet]
        if conf >= minConf:
            print(midSet, "------>", freqSet-midSet, conf)
            ruleList.append((midSet, freqSet-midSet, conf))  # 以三元组形式记录关联规则

def rules_from_complex_set(ruleList, complexSet, H, supData, minConf):
    l = len(H)  # 查看该复杂set元素的个数
    for i in range(1, l-1):  # eg:复杂set有3个元素,则生成规则有 1个--->2个， 2个--->1个
        if i == 1:
            calConf(ruleList, complexSet, H, supData, minConf)
        else:
            midSet = aprigen(H)
            while(len(midSet[0]) != i):
                midSet = aprigen(midSet)  # 循环调用aprigen函数，生成含有i个元素的set
            calConf(ruleList, complexSet, midSet, supData, minConf)


def generateRules(L, supportData, minConf=0.5):
    ans_rules_list = []
    for i in range(1, len(L)-1):
        for single_set in L[i]:
            H = [frozenset([item]) for item in single_set]
            if i == 1:
                calConf(ans_rules_list, single_set, H, supportData, minConf)
            else:
                rules_from_complex_set(ans_rules_list, single_set, H, supportData, minConf)
    return ans_rules_list
if __name__ == "__main__":
    data = loadData()
    #print("原始交易数据:", data)
    c1 = createC1(data)
    #print("c1:", c1)
    L1, supData = Filter(data, c1, minSup=0.5)
    # print("L1:", L1)
    # print("supdata:", supData)
    L = []
    k = 2
    L.append(L1)
    while len(L[k-2]) > 0:
        ck = aprigen(L[k-2])
        Lk, sup = Filter(data, ck, minSup=0.5)
        supData.update(sup)
        L.append(Lk)
        k += 1
    print("当前L：", L)
    print("supdata:", supData)
    generateRules(L, supData, 0.5)