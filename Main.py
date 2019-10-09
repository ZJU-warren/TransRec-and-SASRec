import sys ;sys.path.append('../')
import A_PreProcessing.B_Gen_RelItemSet as AB
import B_DataPartition.A_DataSplit as BA
import C_ModelTrain.TransRec as TransRec
import DataLinkSet as DLSet
import Redirection as RD
import sys
import os


def Main():
    for each in DLSet.dataSet:
        DLSet.dataSetChoice = each
        print('-----------------------------------')
        print(DLSet.dataSetChoice)
        AB.Main()
        BA.Main()
        TransRec.Main()


if __name__ == '__main__':
    Main()
