import numpy as np
from math import *


def load_training_data():
    train_data = []
    label = []
    with open("training-data")as f:
        for line in f.readlines():
            temp = line.strip().split()
            train_data.append(temp[:-1])
            label.append(int(temp[-1]))
    return train_data, label


def crea_voca_list(train_data):
    voca_list = set([])
    for doc in train_data:
        voca_list = voca_list | set(doc)
    return list(voca_list)


def word2vec(voca_list, doc):
    doc_vec = [0] * len(voca_list)
    for word in doc:
        if word in voca_list:
            doc_vec[voca_list.index(word)] = 1
        else:
            print("the word %s is not in the voca_list" % word)
    return doc_vec


# 核心函数，用到其他小辅助函数
def trainNB(train_data, label):
    # 这是一个二分类，若多分类则代码应修改
    # 首先将原始train_data--->train_data_vec
    pclass1 = sum(label)/float(len(train_data))  # p1表示文档属于类别1的概率
    train_data_vec = []
    voca_list = crea_voca_list(train_data)
    for doc in train_data:
        train_data_vec.append(word2vec(voca_list, doc))

    p1num = np.ones(len(train_data_vec[0]))
    p0num = np.ones(len(train_data_vec[0]))
    p1total = len(train_data_vec[0])  # 此处存疑，书上初始化为2
    p0total = len(train_data_vec[0])

    for i in range(len(train_data)):  # 对每篇文档
        if label[i] == 1:
            p1num += train_data_vec[i]
            p1total += sum(train_data_vec[i])
        else:
            p0num += train_data_vec[i]
            p0total += sum(train_data_vec[i])
    p1vec = np.log(p1num/p1total)
    p0vec = np.log(p0num/p0total)
    return pclass1, p1vec, p0vec, voca_list


def classifyNB(test_vec, p0vec, p1vec, p1class):
    p1 = sum(test_vec*p1vec) + log(p1class)
    p0 = sum(test_vec*p0vec) + log(1-p1class)
    if p1 > p0:
        return 1
    else:
        return 0


def test_parse(doc):
    """
    将单篇文档解析成词汇表
    :param doc:
    :return:set[]
    """
    import re
    list_tokens = re.split(r'\W+', doc)
    return [tok.lower() for tok in list_tokens if len(tok) > 2]


def simple_bayes_test():
    train_data, label = load_training_data()
    test_doc = ['love', 'my', 'dalmation']
    p1, p1v, p0v, voca_list = trainNB(train_data, label)
    print(p1, p1v, p0v)
    print("the", test_doc, "is classified as %d" % classifyNB(word2vec(voca_list, test_doc), p0v, p1v, p1))


def email_test():
    import random
    """
    朴素贝叶斯应用：垃圾email分类
    :return:
    """
    email_label = []
    word_list = []
    test_data = []
    test_label = []
    word = []
    correct = 0  # 正确判断的个数
    for i in range(1, 26):  # 每类邮件有25个doc
        # 非垃圾1
        word = test_parse(open("ham/%d.txt" % i).read())  # word是单篇邮件的词汇集合
        word_list.append(word)  # word_list是所有邮件汇总的词汇集合
        email_label.append(1)
        # 垃圾0
        doc_list = open("spam/%d.txt" % i).read()
        word_list.append(test_parse(doc_list))
        email_label.append(0)
        p1, p1v, p0v, vo_list = trainNB(word_list, email_label)
    #  随机挑选十个作为测试集, 为了避免重复，此处选一个删一个!!
    for i in range(10):
        rand_index = random.randint(0, len(word_list)-1)  # 此处不能用49, 只能用len(word_list)
        print(rand_index)
        if rand_index >= len(word_list):
            print("error, the length of word_list is %d, but the rand_index is %d" % (len(word_list), rand_index))
            return 0
        test_label.append(email_label[rand_index])
        test_data.append(word_list[rand_index])
        del(word_list[rand_index])

    for i in range(10):  #开始测试
        test_vec = word2vec(vo_list, test_data[i])
        final_class = classifyNB(test_vec, p0v, p1v, p1)
        if final_class == test_label[i]:
            correct += 1
    return correct/10
if __name__ == "__main__":
    rate = email_test()
    print(rate)

    #simple_bayes_test()


