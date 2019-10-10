import sys ;sys.path.append('../')
import DataLinkSet as DLSet
from tools import *
from collections import defaultdict


# 将原始数据处理为csv表, 并进行频率统计
def Handle(dataSetChoice):
    count_U = defaultdict(lambda: 0)     # 统计用户出现次数
    count_I = defaultdict(lambda: 0)     # 统计物品出现次数

    with open(DLSet.orgData_reviewsParse_link % dataSetChoice, 'w') as f:
        with open(DLSet.orgData_reviews_link % dataSetChoice, 'r') as fData:
            dataSet = fData.readlines()
            print('total reviews: ', len(dataSet))
        flag = 0
        for aLine in dataSet:
            each = aLine[:-1].split(',')
            # 存储记录
            if len(each) == 4:
                f.write(" ".join([each[0], each[1], each[2], each[3]]) + '\n')
            else:
                print(each)
            # 属性提取
            userID = each[0]
            itemID = each[1]
            # timeStamp = each['unixReviewTime']

            # 数据统计
            count_U[userID] += 1
            count_I[itemID] += 1

    return count_U, count_I


# 完成keyID映射, 数据量大时可用BST优化
def MapID(keyID, keyMapSet, count):
    flag = False
    if keyID in keyMapSet:
        keyID = keyMapSet[keyID]
        flag = True
    else:
        keyMapSet[keyID] = count
        keyID = count
        count += 1
    return keyID, count, flag


# 按照数量进行过滤
def Fliter(count_U, count_I, dataSetChoice):
    userMapSet = {}     # 将用户映射到 [0, 1, ..] 区间中
    itemMapSet = {}     # 将物品映射到 [0, 1, ..] 区间中

    userAction = {}     # 记录用户和物品之间交互记录, keyID 为 映射后的用户ID
    count_user = 0
    count_item = 0

    with open(DLSet.orgData_reviews_link % dataSetChoice, 'r') as fData:
        dataSet = fData.readlines()
    for aLine in dataSet:
        each = aLine[:-1].split(',')

        # 属性提取
        userID = each[0]
        itemID = each[1]
        timeStamp = each[3]

        # 过滤出现次数少的用户和物品记录
        if count_U[userID] < DLSet.LIMIT_EXIST_TIMES or count_I[itemID] < DLSet.LIMIT_EXIST_TIMES:
            continue

        # 完成ID映射
        userID, count_user, flagU = MapID(userID, userMapSet, count_user)
        itemID, count_item, flagI = MapID(itemID, itemMapSet, count_item)

        # 若为新用户, 初始化其评论列表
        if flagU is False:
            userAction[userID] = []
        # 添加记录
        userAction[userID].append([timeStamp, itemID])

    # 对每个用户的行为按交互时间进行升序
    for userID in userAction.keys():
        userAction[userID].sort(key=lambda x: x[0])
    # print(userAction[0])

    print('total items:', count_item)
    print('total users:', count_user)
    return userMapSet, itemMapSet, userAction, count_user, count_item


if __name__ == '__main__':
    dataSetChoice = DLSet.dataSet[0]
    count_U, count_I = Handle(dataSetChoice)
    userMapSet, itemMapSet, userAction, count_user, count_item = Fliter(count_U, count_I, dataSetChoice)

