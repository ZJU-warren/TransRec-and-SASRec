import sys ;sys.path.append('../')
import A_PreProcessing.A_Gen_UISet_AmazonRating as AA
import DataLinkSet as DLSet
from tools import *



# 整合出物品的相关属性
def GenRelItemSet(itemMapSet):
    IIG = {}
    # 相关关系
    Relationships = ['also_bought', 'also_viewed', 'bought_together', 'buy_after_viewing']

    for each in Parse(DLSet.orgData_meta_link):
        # 属性提取
        itemID = each['asin']

        # 映射ID
        if itemID not in itemMapSet:
            continue
        print('hit')
        itemID = itemMapSet[itemID]

        # 初始化信息
        IIG[itemID] = {}
        IIG[itemID]['related'] = {}
        for rel in Relationships:
            IIG[itemID]['related'][rel] = []

        # 若有相关物品信息
        if 'related' in each:
            for rel in each['related']:
                for rel_Item in each['related'][rel]:
                    if rel_Item in itemMapSet:
                        IIG[itemID]['related'][rel].append(itemMapSet[rel_Item])

        # 记录物品类别
        IIG[itemID]['categories'] = each['categories']

        if itemID == 0:
            print(IIG[itemID])

    return IIG


def Main():
    count_U, count_I = AA.Handle()
    userMapSet, itemMapSet, userAction, count_user, count_item = AA.Fliter(count_U, count_I)
    # IIG = GenRelItemSet(itemMapSet)
    IIG = {}
    genDataSet = [userAction, IIG, userMapSet, itemMapSet, count_user, count_item]
    np.save(DLSet.mainData_link, genDataSet)


if __name__ == '__main__':
    Main()