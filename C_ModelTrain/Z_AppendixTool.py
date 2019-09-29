import sys ;sys.path.append('../')
import DataLinkSet as DLSet
from tools import *


# sigmod 函数
def sigmoid(x):
    return 1.0 / (1 + exp(-x))


# 生成物品转移图
def Gen_ItemSuccessor(UT, count_item):
    itemSuccessor = [[] for _ in range(count_item)]
    for user in UT:
        # print(UT[user])
        for i in range(len(UT[user]) - 1):
            pre = UT[user][i]
            suc = UT[user][i + 1]
            itemSuccessor[pre].append(suc)
            # print(pre, suc)
    numRel = sum(len(itemSuccessor[item]) for item in range(count_item))
    return itemSuccessor, numRel


# 随机获取一个序长为2以上的用户行为序列
def GetAUser(UT, count_user):
    while True:
        user = random.randint(0, count_user-1)
        if len(UT[user]) > 1:
            return user


# 随机获取一个与当前物品不同的物品
def FindNegSucc(pos_item, count_item):
    while True:
        neg_item = random.randint(0, count_item - 1)
        if neg_item != pos_item:
            return neg_item


