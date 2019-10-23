import sys
from collections import defaultdict
import random


def process_data():
    random.seed(123456)
    fMETDataFileNew = open(sys.argv[1], 'r')
    fLDAOutputFile = open(sys.argv[2], 'w')
    fCrossvalidationID = open('/'.join(sys.argv[1].split('/')[0:-1]) + '/CV-ID.csv', 'w')

    lstPatients = (fMETDataFileNew.readline().strip(' \n')).split(',')
    lstPatients.pop(0)
    print("Number of patients: ", len(lstPatients))
    iTotalPatients = len(lstPatients)

    for iLoop in range(0, 20):

        iStart = iLoop * 100 + 1
        iEnd = iStart + 100
        # iStart = 1
        # iEnd = len(lstPatients)+1
        iIndex = 0

        if iStart > iTotalPatients:
            break

        if iEnd > iTotalPatients:
            iEnd = iTotalPatients + 1

        print(iStart, iEnd)

        fMETDataFileNew.seek(0, 0)
        lstPatients = (fMETDataFileNew.readline().strip(' \n')).split(',')
        lstPatients.pop(0)
        dicMETData = defaultdict(dict)

        for sLine in fMETDataFileNew:
            sFields = (sLine.strip(' \t\n')).split(',')

            for i in range(iStart, iEnd):
                dicMETData[lstPatients[i - 1]][sFields[0]] = sFields[i]

        lstGenes = dicMETData[lstPatients[iStart]].keys()
        iCountGenes = len(dicMETData[lstPatients[iStart]].keys())
        print(len(dicMETData))
        print(iCountGenes)

        sOut = ""
        iGeneCount = 0
        for j in range(iStart, iEnd):

            sOut = ""
            iGeneCount = 0
            for k in range(iCountGenes):
                if dicMETData[lstPatients[j - 1]][lstGenes[k]] != 'N':
                    sOut = sOut + str(k) + ':' + \
                           (dicMETData[lstPatients[j - 1]][lstGenes[k]]) + ' '
                    iGeneCount = iGeneCount + 1
            sOut = str(iGeneCount) + ' ' + sOut

            if iGeneCount == 0:
                sOut = ""
                for k in range(iCountGenes):
                    sOut = sOut + str(k) + ':1 '

                sOut = str(iCountGenes) + ' ' + sOut

            fLDAOutputFile.writelines(sOut + '\n')
            fCrossvalidationID.writelines(str(random.randint(1, 5)) + '\n')

        fLDAOutputFile.flush()

    open(sys.argv[2] + '-Gene_List', 'w').writelines('\n'.join(lstGenes))
    fLDAOutputFile.close()
    fMETDataFileNew.close()
    fCrossvalidationID.close()


if __name__ == '__main__':
    sys.exit(process_data())
