"""
    每行视为一个用户, 并且添加时间戳
"""

import DataLinkSet as DLSet
from tools import *


def MapStr2Int(dfOrg, str, mapLink):
    df = dfOrg.drop_duplicates([str], keep='last')[[str]]

    # 生成映射表
    df['tempMark'] = 1
    df[str + 'ID'] = df.groupby(['tempMark']).cumcount() + 1
    df[[str+'ID', str]].to_csv(mapLink, index=False)

    # 原表和映射表合并
    dfOrg = pd.merge(dfOrg, df, on=[str])
    # print(dfOrg.head(5))

    # 替换后删掉多余列
    dfOrg[str] = dfOrg[str + 'ID']

    # print(dfOrg.head(5))

    dfOrg.drop(columns=[str + 'ID'])
    # print(dfOrg.head(5))

    return dfOrg


def Main():
    # for each in DLSet.dataSet:
    each = 'MovieLens'
    df = pd.read_csv(open(DLSet.orgData_reviews_link % each, 'r'),
                     header=None, names=['user', 'item', 'score', 'timeStamp'])

    df = MapStr2Int(df, 'item', DLSet.mapItemID_SAS_link % each)
    df = MapStr2Int(df, 'user', DLSet.mapItemID_SAS_link % each)
    df = df.sort_values(by=['userID', 'timeStamp'])

    df['act'] = df.groupby(['userID']).cumcount() + 1
    df = df.drop_duplicates(['userID'], keep='last')
    print(df[['act']].describe())

    df.to_csv(DLSet.data_SAS_link % each, sep=' ', header=None, index=False, columns=['userID', 'itemID'])


if __name__ == '__main__':
    Main()
