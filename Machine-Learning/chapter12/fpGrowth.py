def loadData(filename):
    simpleDat = []
    f = open(filename)
    for line in f.readlines():
        simpleDat.append(line.strip().split())
    return simpleDat


class treeNode:
    def __init__(self, nameVal, countVal, parentNode):  # 节点创建时并不知孩子节点，故不需要child参数
        self.name = nameVal
        self.count = countVal
        self.parent = parentNode
        self.nodeLink = None  # 指向相似节点
        self.children = {}

    def incre(self, numIncre):
        self.count += numIncre

    def display(self, indent=1):
        print("  " * indent, self.name, "  ", self.count)  # 输出自己
        for child in self.children.values():
            child.display(indent + 1)


def dataInit(dataset):
    data_dic = {}
    for item in dataset:
        data_dic[frozenset(item)] = data_dic.get(frozenset(item), 0) + 1
    #print("数据最开始的字典形式:", data_dic)
    return data_dic


def updateHeadList(nodeBegin, nodeEnd):
    while nodeBegin.nodeLink != None:
        nodeBegin = nodeBegin.nodeLink
    nodeBegin.nodeLink = nodeEnd


def updateTree(orderItem, myTree, count, headList):  # myTree 最开始是一个空节点（"nullset", 1, None）
    firItem = orderItem[0]
    if firItem in myTree.children:
        myTree.children[firItem].incre(count)
    else:
        myTree.children[firItem] = treeNode(firItem, count, myTree)
        if headList[firItem][1] == None:
            headList[firItem][1] = myTree.children[firItem]
        else:
            updateHeadList(headList[firItem][1], myTree.children[firItem])
    if len(orderItem) > 1:  # 对剩下的元素迭代调用updateTree
        updateTree(orderItem[1::], myTree.children[firItem], count, headList)
    # print("执行到updateTree")
    return


def createTree(dataSet, minsup):  # minsup最少频次
    headList = {}
    # 第一次遍历，统计词频
    for dtset, num in dataSet.items():
        for item in dtset:
            headList[item] = headList.get(item, 0) + num
    #print("第一次遍历统计词频时的表头字典:(未删减)", headList)
    for i in list(headList.keys()):  # 删除不符合minsup的元素, 用list转换，否则报错（字典遍历时不能修改字典元素)
        if headList[i] < minsup:
            del (headList[i])  # headList 记录全部高频元素频次
    #print("删减后的headList", headList)
    freItem = [v[0] for v in sorted(headList.items(), key=lambda x: x[1], reverse=True)]  # 规定排序顺序
    #freItem = ['z', 'x', 'y', 's', 'r', 't']
    # print("固定排序顺序freItemSet:", freItem)
    if len(freItem) == 0:  # 集和都是非频繁项，返回空
        return None, None
    for key in headList:
        headList[key] = [headList[key], None]  # 扩展一个空指针
    myTree = treeNode("nullSet", 1, None)
    #print("\n**********对每个原始集和进行去非频繁且排序")
    for dtset, num in dataSet.items():
    #    print("当前dtset:", dtset)
        temp_dic = {}
        for item in dtset:
            if item in freItem:
                if item == 'z':
                    pass
                    #print("come,here")
                temp_dic[item] = headList[item][0]
        orderItem = [v[0] for v in sorted(temp_dic.items(), key=lambda x: x[1], reverse=True)]  # 先按频次高低排列
        orderItem.sort(key=lambda x: freItem.index(x), reverse=False)  # 再按出现先后排列
        # print(orderItem)
        if len(temp_dic) > 0:  # 原始数据全为非频繁项
            updateTree(orderItem, myTree, num, headList)
    return myTree, headList


def findSinglePrePath(node, prefixPath):
    if node.parent != None:
        prefixPath.append(node.name)
        findSinglePrePath(node.parent, prefixPath)
    return prefixPath


def findAllPrefixPath(baseNodeName, headList):
    Path_dic = {}
    node = headList[baseNodeName][1]
    while node != None:
        prefixPath = []
        findSinglePrePath(node, prefixPath)
        if len(prefixPath) > 1:
            Path_dic[frozenset(prefixPath[1:])] = node.count
        node = node.nodeLink
    return Path_dic


def mineTree(myTree, headTable, minsup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headTable.items(), key=lambda x: x[1][0])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBases = findAllPrefixPath(basePat, headTable)
        mycondTree, myHead = createTree(condPattBases, minsup)
        if myHead != None:
        #    print("conditional tree for:", newFreqSet)
            mycondTree.display()
            mineTree(mycondTree, myHead, minsup, newFreqSet, freqItemList)


if __name__ == "__main__":
    data = dataInit(loadData("simpDat"))
    myTree, headTable = createTree(data, 3)
    myTree.display()
    #print("headTable:", headTable)
    #print(sorted(headTable.values(), key=lambda x: x[0]))
    #print("r的所有前缀路径:", findAllPrefixPath('r', headTable))
    freqItems = []
    mineTree(myTree, headTable, 3, set([]), freqItems)
    print(freqItems)
