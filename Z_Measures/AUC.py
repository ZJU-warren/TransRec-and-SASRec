import sys ;sys.path.append('../')
from tools import *

class MyAUC:
    aucSum = 0
    totalN = 0                              # total #event == #Update

    def Update(self, baseP, negPSet):
        self.totalN += 1
        sumScore = 0
        for each in negPSet:
            if each < baseP:
                sumScore += 1
            elif each == baseP:             # 源代码有问题
                sumScore += 0.5
        self.aucSum += sumScore / len(negPSet)

    def GetAUC(self):
        res = self.aucSum / self.totalN
        return res


# 指标评估
def Measure(model, UT, UV, UJ, count_item, negN=100):
    # 定义评价指标
    aucAgent_T = MyAUC()
    aucAgent_V = MyAUC()
    aucAgent_J = MyAUC()

    for user in UJ:
        if len(UT[user]) < 2 or len(UJ[user]) == 0:
            continue
        """ 获取真实结果的预测值 """
        baseScore_T = model.TransPredict(user, UT[user][-2], UT[user][-1])
        baseScore_V = model.TransPredict(user, UV[user][0], UV[user][1])
        baseScore_J = model.TransPredict(user, UJ[user][0], UJ[user][1])

        # 负样本评分集合初始化
        negPSet_T = []
        negPSet_V = []
        negPSet_J = []

        # 利用negN个负样本作为评分依据
        _ = 0
        while _ < negN:
            negItem = random.randint(0, count_item - 1)
            if negItem not in UT[user] and negItem not in UJ[user]:
                _ += 1
                negPSet_T.append(model.TransPredict(user, UT[user][-2], negItem))
                negPSet_V.append(model.TransPredict(user, UV[user][0], negItem))
                negPSet_J.append(model.TransPredict(user, UJ[user][0], negItem))

        aucAgent_T.Update(baseScore_T, negPSet_T)
        aucAgent_V.Update(baseScore_V, negPSet_V)
        aucAgent_J.Update(baseScore_J, negPSet_J)

    return aucAgent_T.GetAUC(), aucAgent_V.GetAUC(), aucAgent_J.GetAUC()

