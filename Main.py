import sys ;sys.path.append('../')
import A_PreProcessing.B_Gen_RelItemSet as AB
import B_DataPartition.A_DataSplit as BA
import C_ModelTrain.TransRec as TransRec
import DataLinkSet as DLSet
import sys
import os


def Main():
    for each in DLSet.dataSet:
        print('-----------------------------------')
        print(each)
        # AB.Main(each)
        # BA.Main(each)
        TransRec.Main(each)


if __name__ == '__main__':
    Main()
