import sys ;sys.path.append('../')
import A_PreProcessing.B_Gen_RelItemSet as AB
import B_DataPartition.A_DataSplit as BA
import C_ModelTrain.TransRec as TransRec


def Main():
    AB.Main()
    BA.Main()
    TransRec.Main()


if __name__ == '__main__':
    Main()