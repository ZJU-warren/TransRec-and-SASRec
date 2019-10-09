"""
修改文件为csv, sep=','
其中tagID更变为
文件名更变
"""

import DataLinkSet as DLSet
from tools import *


def EX():
    df = pd.read_csv(DLSet.RawSetLink + '/Raw_LastFM.dat', sep='\t')
    df.to_csv(DLSet.RawSetLink + '/Raw_LastFM', header=None, index=None)


if __name__ == '__main__':
    EX()
