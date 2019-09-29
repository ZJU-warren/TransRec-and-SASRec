import sys ;sys.path.append('../')
from tools import *

class MyHitRatio:
    hrSum = 0
    totalN = 0                              # total #event == #Update

    # 初始化限制数目
    def __init__(self, limit):
        self.limit = limit

    def Update(self, item, negPSet):
        # print(item, negPSet[:self.limit])
        self.totalN += 1
        if item in negPSet[:self.limit]:
            self.hrSum += 1

    def GetHR(self):
        # print(self.hrSum)
        return self.hrSum / self.totalN


# 排序且只保留关键字
def listSort(li, isRverse=True):
    li = sorted(li, key=lambda each: each[0], reverse=isRverse)
    li = [each[1] for each in li]
    return li


# 指标评估
def Measure(model, UT, UV, UJ, count_item, limit=50, subN=200):
    # 定义评价指标
    hrAgent_T = MyHitRatio(limit)
    hrAgent_V = MyHitRatio(limit)
    hrAgent_J = MyHitRatio(limit)
    uC = 0
    for user in UJ:
        uC += 1
        print("-------- %d/%d user --------" % (uC, len(UJ)))
        if len(UT[user]) < 2 or len(UJ[user]) == 0:
            continue

        # 负样本评分集合初始化
        subPSet_T = []
        subPSet_V = []
        subPSet_J = []

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
        hrAgent_T.Update(UT[user][-1], subPSet_T)
        hrAgent_V.Update(UV[user][1], subPSet_V)
        hrAgent_J.Update(UJ[user][1], subPSet_J)
        print(hrAgent_J.GetHR())
    return hrAgent_T.GetHR(), hrAgent_V.GetHR(), hrAgent_J.GetHR()


if __name__ == '__main__':
    li = [(3, 'a'), (2, 'c'), (1, 'b')]
    li = listSort(li, True)
    print(li)
