import sys ;sys.path.append('../')
import DataLinkSet as DLSet
import pandas as pd
import time
import gzip
import datetime

orgHeader = ['userID', 'itemID', 'score', 'timeStamp']


# 数据处理器
def Parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


# 加载数据
def LoadData(datalink, sep=','):
    return pd.read_csv(open(datalink, 'r'), sep=sep)


# 按给定时间划分
def SampleByTime(dataLink, storeLink, timeLimit):
    print('****** SampleByTime ******')
    # 清空原有数据, 没有则创建文件
    with open(storeLink, 'w') as f:
        f.truncate()

    maxT = -1
    minT = 99999999999999
    with open(storeLink, 'w') as f:
        for each in Parse(dataLink):
            if 'unixReviewTime' in each and each['unixReviewTime'] is not None:
                if each['unixReviewTime'] >= timeLimit:
                    # 存储记录
                    f.write(",".join([str(each['gPlusUserId']), str(each['gPlusPlaceId']),
                                      str(each['rating']), str(each['unixReviewTime'])]) + '\n')

                    # print(each['unixReviewTime'])
                    maxT = max(maxT, each['unixReviewTime'])
                    minT = min(minT, each['unixReviewTime'])

    dt1 = datetime.datetime.fromtimestamp(maxT)
    dt2 = datetime.datetime.fromtimestamp(minT)
    print(dt1.strftime("%Y--%m--%d %H:%M:%S"))
    print(dt2.strftime("%Y--%m--%d %H:%M:%S"))
    print('****** End: SampleByTime ******')


# 生成key出现次数表
def GenKeyIDTimeTable(dataLink, storeLink, keyWord):
    print('****** GenKeyIDTimeTable ******')
    # 清空原有数据, 没有则创建文件
    with open(storeLink, 'w') as f:
        f.truncate()

    # 分块读取
    batch = 1
    for df in pd.read_csv(open(dataLink, 'r'), chunksize=100000, header=None, names=orgHeader):
        # print('Processing the %d batch' % batch)
        try:
            df[[keyWord]].to_csv(open(storeLink, 'a'), index=None, header=None)
            batch += 1
        except StopIteration:
            print("Iteration is stopped.")
            break

    # 统计频率
    dfCount = pd.read_csv(open(storeLink, 'r'), header=None, names=[keyWord])
    dfCount['Count_%s' % keyWord] = dfCount.groupby([keyWord]).cumcount() + 1
    dfCount = dfCount.drop_duplicates([keyWord], keep='last')

    print('****** End: GenKeyIDTimeTable ******')
    return dfCount


# 过滤掉低于阈值的数据
def Filter(dataLink, storeLink, keyWord, threshold):
    print('****** Filter ******')
    # 获取需要保留的KeyID
    dfCount = GenKeyIDTimeTable(dataLink, DLSet.tempTable_link, keyWord)
    dfCount = dfCount[dfCount['Count_%s' % keyWord] >= threshold][[keyWord]]

    # 清空原有数据, 没有则创建文件
    with open(storeLink, 'w') as f:
        f.truncate()

    # 分块读取
    totalShape = 0
    batch = 1
    for df in pd.read_csv(open(dataLink, 'r'), chunksize=100000, header=None, names=orgHeader):
        # print('Processing the %d batch' % batch)
        try:
            df = pd.merge(df, dfCount, on=[keyWord])
            df.to_csv(open(storeLink, 'a'), index=None, header=None)

            totalShape += df.shape[0]
            batch += 1
        except StopIteration:
            print("Iteration is stopped.")
            break

    # print('Left %d %ss and %d ratings' % (dfCount.shape[0], keyWord, totalShape))

    print('****** End: Filter ******')


# 获取K-core
def GenKCore(dataLink, storeLink, K):
    print('****** GenKCore ******')
    """
        # 获取 ratings 大于K的用户
        Filter(dataLink, DLSet.tempTable_link, keyWord, K)
        df = pd.read_csv(open(DLSet.tempTable_link, 'r'), header=None, names=orgHeader)
    """
    df = pd.read_csv(open(dataLink, 'r'), header=None, names=orgHeader)

    # 统计d(userID) <= K
    keyWord = 'userID'
    df['count_%s' % keyWord] = df.groupby([keyWord]).cumcount() + 1
    df = df[df['count_%s' % keyWord] <= K][orgHeader]

    # 统计d(itemID) <= K
    keyWord = 'itemID'
    df['count_%s' % keyWord] = df.groupby([keyWord]).cumcount() + 1
    df = df[df['count_%s' % keyWord] <= K][orgHeader]

    df.to_csv(storeLink, header=None, index=False)

    # print('ratings : %d' % df.shape[0])
    print('****** End: GenKCore ******')


# 对keyID采样
def GenSample(dataLink, storeLink, keyWord, frac):
    dfU = GenKeyIDTimeTable(dataLink, DLSet.tempTable_link, keyWord)[[keyWord]].sample(frac=frac)

    # 清空原有数据, 没有则创建文件
    with open(storeLink, 'w') as f:
        f.truncate()

    # 分块读取
    totalShape = 0
    batch = 1
    for df in pd.read_csv(open(dataLink, 'r'), chunksize=100000, header=None, names=orgHeader):
        print('Processing the %d batch' % batch)
        try:
            df = pd.merge(df, dfU, on=[keyWord])
            df.to_csv(open(storeLink, 'a'), index=None, header=None)

            totalShape += df.shape[0]
            batch += 1
        except StopIteration:
            print("Iteration is stopped.")
            break

    # print('Left %d %ss and %d ratings' % (dfU.shape[0], keyWord, totalShape))


# 统计每个维度id数目
def GiveMeTheNumber(dataLink):
    df = pd.read_csv(open(dataLink, 'r'), header=None, names=orgHeader)
    print('-----------------------------------------------')
    print("# ratings: ", df.shape[0])
    for each in orgHeader:
        if each != 'score':
            dfX = df[[each]].drop_duplicates([each], keep='last')
            print('# ' + each + ':', dfX.shape[0])


# 主函数
def Main():
    # 按时间抽取数据
    print('------------------- 按时间抽取数据 --------------------')
    # SampleByTime(DLSet.rawRatings_link, DLSet.rawRatings_Sample_link, DLSet.TIME_LIMIT)
    GiveMeTheNumber(DLSet.rawRatings_Sample_link)
    # 处理出现次数低于阈值的物品
    print('------------------- 处理出现次数低于阈值的物品 --------------------')
    Filter(DLSet.rawRatings_Sample_link, DLSet.filter_item_link, 'itemID', DLSet.LIMIT_EXIST_TIMES)

    # 处理出现次数低于阈值的用户
    print('------------------- 处理出现次数低于阈值的用户 --------------------')
    Filter(DLSet.filter_item_link, DLSet.filter_user_link, 'userID', DLSet.USER_TIME_LIMIT)
    GiveMeTheNumber(DLSet.filter_user_link)

    print('------------------- 取样 --------------------')
    frac = 0.3
    GenSample(DLSet.filter_user_link, DLSet.sample_afterFilter_link % str(frac), 'userID', frac)
    GiveMeTheNumber(DLSet.sample_afterFilter_link % str(frac))

    # K-Core
    print('------------------- K-core --------------------')
    K = 20
    GenKCore(DLSet.filter_user_link, DLSet.KCore_link % K, K)
    GiveMeTheNumber(DLSet.KCore_link % K)

    K = 10
    GenKCore(DLSet.filter_user_link, DLSet.KCore_link % K, K)
    GiveMeTheNumber(DLSet.KCore_link % K)


if __name__ == '__main__':
    Main()



####
#### 2014--03--29 16:39:20
#### 1990--12--31 08:00:00
####