"""
    每行视为一个用户, 并且添加时间戳
"""

import DataLinkSet as DLSet
from tools import *


def EX():
    cntU = 0
    with open('../' + DLSet.RawSetLink + '/Raw_YooChoose', 'w') as wf:
        with open('../' + DLSet.RawSetLink + '/yoochoose_click_dense.txt', 'r') as f:
            while True:
                line = f.readline()
                if line:
                    cntU += 1
                    tim = 0
                    aList = line[:-1].split(' ')
                    for each in aList:
                        tim += 1
                        wf.write(str(cntU) + ',' + each + ',1,' + str(tim) + '\n')  # flag标记没有实际意义
                else:
                    break


if __name__ == '__main__':
    EX()
