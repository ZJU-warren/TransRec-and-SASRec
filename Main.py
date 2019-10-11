import sys ;sys.path.append('../')
import A_PreProcessing.B_Gen_RelItemSet as AB
import B_DataPartition.A_DataSplit as BA
import C_ModelTrain.TransRec as TransRec
import DataLinkSet as DLSet
import sys
import os


def Main():
    for each in ['MovieLens', 'YooChoose', 'Google']:
        print('-----------------------------------')
        print(each)
        AB.Main(each)
        print('*** end AB')
        BA.Main(each)
        print('*** end BA')
        TransRec.Main(each)


if __name__ == '__main__':
    Main()


# scp -r wr@10.214.192.11:/wr/home/Project/ Project/