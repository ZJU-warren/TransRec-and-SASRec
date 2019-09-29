import sys ;sys.path.append('../')
from C_ModelTrain.Z_AppendixTool import *
from collections import defaultdict
import Z_Measures.AUC as AUC
import Z_Measures.HitRatio as HR
import Z_Measures.NDCG as NDCG

# 后继推荐
class SuccRec:
    # 数据相关和参数初始化
    def __init__(self, UT, UV, UJ, count_user, count_item, numRel, itemSuccessor):
        self.UT = UT
        self.UV = UV
        self.UJ = UJ
        self.count_user = count_user
        self.count_item = count_item
        self.numRel = numRel
        self.itemSuccessor = itemSuccessor

    # 构建后继概率转移图
    def SuccTable(self):
        self.succPTable = {}
        i = 0
        for each in self.itemSuccessor:
            self.succPTable[i] = {}
            self.succPTable[i]['total'] = 0
            for succ in each:
                if succ not in self.succPTable[i]:
                    self.succPTable[i][succ] = 0
                self.succPTable[i][succ] += 1
                self.succPTable[i]['total'] += 1
            i += 1

    # 给定后继, 预测概率
    def Predict(self, pre):
        res = []
        for i in range(self.count_item):
            res.append((self.succPTable[pre][i] + 1) / (self.succPTable[pre]['total'] + self.count_item))   # Laplace
        return res

    # 进行预测
    def TransPredict(self, user, pre, cur):
        if cur not in self.succPTable[pre].keys():
            exist = 0
        else:
            exist = self.succPTable[pre][cur]
        return (exist + 1) / (self.succPTable[pre]['total'] + self.count_item)          # Laplace


# 取出数据
def GetData():
    dataset = np.load(DLSet.TVJ_link, allow_pickle=True)
    [UT, UV, UJ, count_user, count_item] = dataset
    return UT, UV, UJ, count_user, count_item


def Main():
    # 加载数据
    UT, UV, UJ, count_user, count_item = GetData()
    # 构建后继关系图
    itemSuccessor, numRel = Gen_ItemSuccessor(UT, count_item)
    # 初始化模型
    model = SuccRec(UT, UV, UJ, count_user, count_item, numRel, itemSuccessor)
    # 模型后继概率构建
    model.SuccTable()

    StoreObj(model, DLSet.model_link % 'SuccRec')
    model = LoadObj(DLSet.model_link % 'SuccRec')


    auc_T, auc_V, aucJ = AUC.Measure(model, UT, UV, UJ, count_item)
    print(auc_T, auc_V, aucJ)
    hr_T, hr_V, hr_J = HR.Measure(model, UT, UV, UJ, count_item, subN=-1)
    print(hr_T, hr_V, hr_J)
    ndcg_T, ndcg_V, ndcg_J = NDCG.Measure(model, UT, UV, UJ, count_item, subN=-1)
    print(ndcg_T, ndcg_V, ndcg_J)
    hr_T, hr_V, hr_J = HR.Measure(model, UT, UV, UJ, count_item, limit=10, subN=-1)
    print(hr_T, hr_V, hr_J)
    ndcg_T, ndcg_V, ndcg_J = NDCG.Measure(model, UT, UV, UJ, count_item, limit=10, subN=-1)
    print(ndcg_T, ndcg_V, ndcg_J)


if __name__ == '__main__':
    Main()
