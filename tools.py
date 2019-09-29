""" Reading the data
    Data can be treated as python dictionary objects.

    A simple script to read any of the above the data is as follows:
"""
import gzip
import pandas as pd
import numpy as np
import random
from math import exp
from math import log
import matplotlib.pyplot as plt
import pickle

# 数据处理器
def Parse(path):
    g = gzip.open(path, 'r')
    for l in g:
        yield eval(l)


# 绘制图片
def ShowPic(xSet, ySet, label='', title='', xLabel='', yLabel=''):
    # 输出结果
    lenElem = len(xSet)
    for i in range(lenElem):
        print(xSet[i], ySet[i])

    # 绘制图形
    plt.plot(xSet, ySet, label=label)
    plt.title(title)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.legend(loc=4)
    plt.grid(True, linewidth=0.3)
    plt.show()


# 存储实例
def StoreObj(obj, storeLink):
    pickle.dump(obj, open(storeLink, 'wb'))


# 读取实例,
def LoadObj(dataLink):
    return pickle.load(open(dataLink, 'rb'))


def LoadData(datalink, sep=','):
    return pd.read_csv(open(datalink, 'r'), sep=sep)