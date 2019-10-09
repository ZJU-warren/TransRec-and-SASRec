import sys ;sys.path.append('../')
import DataLinkSet as DLSet
from tools import *
from C_ModelTrain.Z_AppendixTool import *
import Z_Measures.AUC as AUC
import Z_Measures.HitRatio as HR
import Z_Measures.NDCG as NDCG

# 取出数据
def GetData():
    dataset = np.load(DLSet.TVJ_link, allow_pickle=True)
    [UT, UV, UJ, count_user, count_item] = dataset
    return UT, UV, UJ, count_user, count_item


# 训练 + 预测
class TransRec:
    # 预设模型超参数
    lam = 0.05
    bias_lam = 0.01
    reg_lam = 0.1
    K = 300
    learn_rate = 0.05
    max_iter = 1

    # 数据相关和参数初始化
    def __init__(self, UT, UV, UJ, count_user, count_item, numRel):
        self.UT = UT
        self.UV = UV
        self.UJ = UJ
        self.count_user = count_user
        self.count_item = count_item
        self.numRel = numRel

        self.r = np.zeros(self.K)
        self.R = np.random.rand(count_user, self.K) / 1 - 0.5
        self.H = np.random.rand(count_item, self.K) / 1 - 0.5
        self.beta = np.zeros(count_item)

    # 规范化数据
    def Normalization(self, it):
        dist = np.sqrt(np.sum(np.square(self.H[it, :])))
        if dist > 1:
            self.H[it, :] = self.H[it, :] / dist

    # 进行预测
    def TransPredict(self, user, pre, cur):
        return - self.beta[cur] - np.sum(np.square(self.H[pre, :] + self.r + self.R[user, :] - self.H[cur, :]))

    # 单次训练
    def TrainOneRound(self):
        objective = 0
        for _ in range(self.numRel):
            # 随机获得一个用户
            user = GetAUser(self.UT, self.count_user)
            # 随机获取该用户一个行为序号 (除最后一次)
            pos = random.randint(0, len(self.UT[user]) - 2)

            # 读取相关物品
            preItem = self.UT[user][pos]                                     # previous item
            posItem = self.UT[user][pos + 1]                                 # positive item
            negItem = FindNegSucc(posItem, self.count_item)                  # 随机找一个 negative item

            d1 = self.H[preItem, :] + self.r + self.R[user, :] - self.H[posItem, :]
            d2 = self.H[preItem, :] + self.r + self.R[user, :] - self.H[negItem, :]

            z = sigmoid(-self.beta[posItem] + self.beta[negItem] - np.sum(np.square(d1)) + np.sum(np.square(d2)))

            self.beta[posItem] += self.learn_rate * (-(1 - z) - 2 * self.bias_lam * self.beta[posItem])
            self.beta[negItem] += self.learn_rate * ((1 - z) - 2 * self.bias_lam * self.beta[negItem])

            self.H[preItem, :] += self.learn_rate * ((1 - z) * 2 * (d2 - d1) - 2 * self.lam * self.H[preItem, :])
            self.H[posItem, :] += self.learn_rate * ((1 - z) * 2 * d1 - 2 * self.lam * self.H[posItem, :])
            self.H[negItem, :] += self.learn_rate * ((1 - z) * 2 * (-d2) - 2 * self.lam * self.H[negItem, :])

            self.r += self.learn_rate * ((1 - z) * 2 * (d2 - d1) - 2 * self.lam * self.r)
            self.R[user] = self.learn_rate * ((1 - z) * 2 * (d2 - d1) - 2 * self.reg_lam * self.R[user])

            self.Normalization(preItem)
            self.Normalization(posItem)
            self.Normalization(negItem)

            objective += log(z)
        return objective

    # 训练模型
    def Train(self):
        """
        # 调参参考数据
            auc_T = []
            auc_V = []
            auc_J = []
            xValue = []
        """
        # 迭代训练模型
        for it in range(self.max_iter):
            objective = self.TrainOneRound()
            regularization = objective - self.lam * np.sum(np.square(self.H)) - \
                             self.lam * np.sum(np.square(self.r)) - \
                             self.reg_lam * np.sum(np.square(self.R)) - \
                             self.bias_lam * np.sum(np.square(self.beta))

            print('iteration: ' + str(it + 1) + '\t' + str(regularization) + '\t' + str(objective))

            """
            if (it + 1) % 10 == 0:
                auc = Performance_AUC(self, self.UT, self.UV, self.UJ, self.count_item)
                auc_T.append(auc[0])
                auc_V.append(auc[1])
                auc_J.append(auc[2])
                xValue.append(it + 1)
            """
        """
        # 绘制图像
        ShowPic(xValue, auc_T)
        ShowPic(xValue, auc_V)
        ShowPic(xValue, auc_J)
        """


# 主函数
def Main():
    # 加载数据
    UT, UV, UJ, count_user, count_item = GetData()
    # 计算后代和关系数目
    itemSuccessor, numRel = Gen_ItemSuccessor(UT, count_item)
    model = TransRec(UT, UV, UJ, count_user, count_item, numRel)
    model.Train()

    StoreObj(model, DLSet.model_link % 'TransRec')
    model = LoadObj(DLSet.model_link % 'TransRec')

    auc_T, auc_V, auc_J = AUC.Measure(model, UT, UV, UJ, count_item)    ;print('AUC:', auc_J)
    hr_T, hr_V, hr_J = HR.Measure(model, UT, UV, UJ, count_item, subN=-1)   ;print('HR@50', hr_J)
    hr_T, hr_V, hr_J = HR.Measure(model, UT, UV, UJ, count_item, limit=10, subN=-1) ;print('HR@10', hr_J)
    ndcg_T, ndcg_V, ndcg_J = NDCG.Measure(model, UT, UV, UJ, count_item, subN=-1)   ;print('NDCG@50', ndcg_J)
    ndcg_T, ndcg_V, ndcg_J = NDCG.Measure(model, UT, UV, UJ, count_item, limit=10, subN=-1) ;print('NDCG@10', ndcg_J)


if __name__ == '__main__':
    Main()

