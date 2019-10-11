import os
import time

dataSet = ['Amazon', 'Google', 'MovieLens', 'YooChoose', 'LastFM']
dataSetChoice = dataSet[4]                          # 所选用的数据集合

""" 文件夹地址 """
DataSetLink = '../DataSet'                          # 数据仓库总地址
# DataSetLink = '../../DataSet'                     # 数据仓库总地址
RawSetLink = DataSetLink + '/RawSet'                # 原生数据仓库地址
OrgSetLink = DataSetLink + '/OrgSet'                # 原始数据仓库地址
CleanSetLink = DataSetLink + '/CleanSet'            # 清洗数据仓库地址
ModelSetLink = DataSetLink + '/ModelSet'

""" ---------------------------------- 原始数据仓库 ------------------------------------ """
# 原始数据
orgData_reviews_link = RawSetLink + '/Raw_%s'                           # 原始数据(review)
orgData_reviewsParse_link = OrgSetLink + '/reviewsParse_%s'             # 解析后的原始数据(review)
orgData_meta_link = OrgSetLink + '/meta_%s.json.gz'                     # 原始数据(metadata)

""" ---------------------------------- 清洗数据仓库 ------------------------------------ """
# 生成后的数据 [userAction, IIG, userMapSet, itemMapSet, count_user, count_item]
mainData_link = CleanSetLink + '/mainData_%s.npy'
TVJ_link = CleanSetLink + '/TVJ_%s.npy'

""" ---------------------------------- 模型仓库 ------------------------------------ """
model_link = ModelSetLink + '/model_%s_%s'

""" ---------------------------------- 常数设置 ------------------------------------ """
LIMIT_EXIST_TIMES = 5       # userID, itemID 至少出现 LIMIT_EXIST_TIMES 次的原始数据被保留
LEN_SEQUENCE_LEN = 3        # 总序列长度
""" ------------------------------------------------------------------------------ """


if __name__ == '__main__':
    # 获得当前工作目录
    print(os.getcwd())

    # 路径测试
    with open(orgData_reviews_link[3:], 'r') as f:
        # print(f.readline())
        f.close()

""" ---------------------------------- 生数据仓库 ------------------------------------ """
# ------------- 相关常数 --------------
# 选择时间左界
STR_TIME_LIMIT = '2014-1-1'                                                 # 选择左界时间
# STR_TIME_LIMIT = '2000-1-1'                                                 # 选择左界时间
TIME_LIMIT = int(time.mktime(time.strptime(STR_TIME_LIMIT, "%Y-%m-%d")))    # 对应时间戳
ITEM_TIME_LIMIT = 5                                                         # 保留至少出现 itemTimeLimit
USER_TIME_LIMIT = 10                                                        # 保留至少出现 userTimeLimit

# ------------- 相关文件 --------------
strTemp = 'MovieLens-1M'
# rawRatings_link = RawSetLink + '/ratings_%s.csv' % strTemp
# rawRatings_link = RawSetLink + '/reviews.clean.json.gz'
rawRatings_link = RawSetLink + '/ml-1m.dat'
rawRatings_Sample_link = RawSetLink + '/rawRatings_Sample_%s_After_%s' % (strTemp, STR_TIME_LIMIT)      # 按照时间划分
filter_item_link = RawSetLink + '/filter_item_%s_After_%s' % (strTemp, STR_TIME_LIMIT)                  # 过滤掉低频物品
filter_user_link = RawSetLink + '/filter_user_%s_After_%s' % (strTemp, STR_TIME_LIMIT)                  # 过滤掉低频用户
sample_afterFilter_link = RawSetLink + '/sample_%s_afterFilter_%s_After_%s' % ('%s', strTemp, STR_TIME_LIMIT)    # 下采样
tempTable_link = RawSetLink + '/tempTable'                                                              # 临时表
KCore_link = RawSetLink + '/KCore_%s_%s_After_%s' % ('%d', strTemp, STR_TIME_LIMIT)                     # K-Core表
mapItemID_SAS_link = RawSetLink + '/mapItemID_SAS_%s'        # SASRec 需要映射itemID从0开始
data_SAS_link = RawSetLink + '/data_SAS_%s.txt'                  # 映射后的结果
