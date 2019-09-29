import sys ;sys.path.append('../')
from tools import *

class MyNDCG:
    ndcgSum = 0
    totalN = 0                              # total #event == #Update

    # 初始化限制数目
    def __init__(self, limit):
        self.limit = limit

    def Update(self, item, negPSet):
        # print(item, negPSet[:self.limit])
        self.totalN += 1
        for i in range(1, self.limit+1):
            if item == negPSet[i-1]:
                self.ndcgSum += 1/log(i + 1, 2)
                break

    def GetHR(self):
        return self.ndcgSum / self.totalN


# 排序且只保留关键字
def listSort(li, isRverse=True):
    li = sorted(li, key=lambda each: each[0], reverse=isRverse)
    li = [each[1] for each in li]
    return li


# 指标评估
def Measure(model, UT, UV, UJ, count_item, limit=50, subN=200):
    # 定义评价指标
    ndcgAgent_T = MyNDCG(limit)
    ndcgAgent_V = MyNDCG(limit)
    ndcgAgent_J = MyNDCG(limit)

    for user in UJ:
        if len(UT[user]) < 2 or len(UJ[user]) == 0:
            continue

        # 负样本评分集合初始化
        subPSet_T = []
        subPSet_V = []
        subPSet_J = []

        # 利用subN个物品作为评分依据
        if subN != -1:
            # 利用subN个物品作为评分依据
            itemSet = [UT[user][-1], UV[user][1], UJ[user][1]]  # 标准答案需要在内
            _ = 3
            while _ < subN:
                rItem = random.randint(0, count_item - 1)
                if rItem not in itemSet:
                    _ += 1
                    itemSet.append(rItem)
        else:
            itemSet = [i for i in range(count_item)]

        for each in itemSet:
            subPSet_T.append((model.TransPredict(user, UT[user][-2], each), each))
            subPSet_V.append((model.TransPredict(user, UV[user][0], each), each))
            subPSet_J.append((model.TransPredict(user, UJ[user][0], each), each))

        # 降序排列可能性
        subPSet_T = listSort(subPSet_T)
        subPSet_V = listSort(subPSet_V)
        subPSet_J = listSort(subPSet_J)

        # 更新
        ndcgAgent_T.Update(UT[user][-1], subPSet_T)
        ndcgAgent_V.Update(UV[user][1], subPSet_V)
        ndcgAgent_J.Update(UJ[user][1], subPSet_J)

    return ndcgAgent_T.GetHR(), ndcgAgent_V.GetHR(), ndcgAgent_J.GetHR()


if __name__ == '__main__':
    li = [(3, 'a'), (2, 'c'), (1, 'b')]
    li = listSort(li, True)
    print(li)

# 0.03201166993160431 0.01752388954047599 0.015368361454912691
# 0.22396026745673964 0.13388427831982902 0.012177142212519736
