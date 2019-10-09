import sys ;sys.path.append('../')
import DataLinkSet as DLSet
from tools import *
import matplotlib
matplotlib.use('Agg')

# 取出数据
def GetData():
    dataset = np.load(DLSet.mainData_link, allow_pickle=True)
    [userAction, IIG, userMapSet, itemMapSet, count_user, count_item] = dataset
    return userAction, IIG, userMapSet, itemMapSet, count_user, count_item


# Keep U-I
def Keep_UI(uA):
    t = 0
    for user in uA:
        uA[user] = [b for a, b in uA[user]]
        t += len(uA[user])
    print('total u-i: %d' % t)


# 划分TVJ
def Split_TVJ(uA):
    user_T = {}
    user_V = {}
    user_J = {}

    seqLen = DLSet.LEN_SEQUENCE_LEN
    for user in uA:
        if len(uA[user]) < seqLen:      # 若比约定序长小, 则有待填充
            user_T[user] = uA[user]
            user_V[user] = []
            user_J[user] = []
        else:
            user_T[user] = uA[user][:-2]      # 去除最后2个
            user_V[user] = uA[user][-3:-1]    # 用最新第3个和第2个为V集
            user_J[user] = uA[user][-2:]      # 最新2个为测试集合

    return user_T, user_V, user_J


# 主函数
def Main():
    # 取出数据
    userAction, IIG, userMapSet, itemMapSet, count_user, count_item = GetData()

    # 保留 <user: [items]>
    Keep_UI(userAction)

    # 划分TVJ集合
    UT, UV, UJ = Split_TVJ(userAction)

    # 持久化数据
    genDataSet = [UT, UV, UJ, count_user, count_item]
    np.save(DLSet.TVJ_link, genDataSet)


if __name__ == '__main__':
    Main()
