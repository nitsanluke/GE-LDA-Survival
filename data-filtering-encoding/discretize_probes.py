# __author__ = 'luke kumar'
import sys
import numpy as np


#####################################################################################################
# Make Normal range of values as N and bin the two tales separately but have same binning number
# Variations
# 1) bin the tales with equal distance
# 2) bin the tales based on standard deviations
# 3) Drop within 1st Std
# 4) Bin equal size 10
def bin_expression_v2_std(lstFields):
    sNewGE = ""
    lstGE = np.array(map(float, lstFields))
    del lstFields

    # std change
    fMeanGE = 0.0
    fStdGE = 1.0
    fNormalRangeStart = fMeanGE - (fStdGE)  # fStdGE
    fNormalRangeEnd = fMeanGE + (fStdGE)  # fStdGE

    lstLow = []
    lstHigh = []
    for i in range(len(lstGE)):
        if lstGE[i] <= fNormalRangeStart:
            lstLow.append(lstGE[i])
        elif lstGE[i] >= fNormalRangeEnd:
            lstHigh.append(lstGE[i])

    # Equal spaced bins
    low_hist, low_bins = np.histogram(lstLow, bins=10)

    # reverse the negative bins to get correct bin numbers (ascending bin numbers for descending values)
    low_bins = low_bins[::-1]

    high_hist, high_bins = np.histogram(lstHigh, bins=10)

    for i in range(len(lstGE)):

        if lstGE[i] <= fNormalRangeStart:
            sNewGE = sNewGE + str(np.digitize([lstGE[i]], low_bins)[0] + 1) + ','

        elif lstGE[i] >= fNormalRangeEnd:
            sNewGE = sNewGE + str(np.digitize([lstGE[i]], high_bins)[0] + 1) + ','

        else:
            sNewGE = sNewGE + 'N,'

    # N and ','
    if set(sNewGE) == set(['N', ',']):
        sNewGE = ""

    elif len(set(sNewGE)) == 2:
        sNewGE = ""

    else:
        sNewGE = sNewGE[0:-1]

    return sNewGE


#####################################################################################################
# Make Normal range of values as N and bin the two tales separately and have two features for each probe
# Variations
# 1) bin the tales with equal distance
# 2) bin the tales based on standard deviations
# 3) Drop within 1st Std
# 4) Bin both ends equal size 10 bins
# FINAL ENCODING USED IN THE PAPER
def bin_expression_v3_std(lstFields):
    sNewGE_Low = ""
    sNewGE_High = ""
    lstGE = np.array(map(float, lstFields))
    del lstFields

    # std change
    fMeanGE = 0.0
    fStdGE = 1.0
    fNormalRangeStart = fMeanGE - (fStdGE)  # fStdGE
    fNormalRangeEnd = fMeanGE + (fStdGE)  # fStdGE

    lstLow = []
    lstHigh = []
    for i in range(len(lstGE)):
        if lstGE[i] <= fNormalRangeStart:
            lstLow.append(lstGE[i])
        elif lstGE[i] >= fNormalRangeEnd:
            lstHigh.append(lstGE[i])

    # Equal spaced 10 bins
    low_hist, low_bins = np.histogram(lstLow, bins=10)

    # reverse the negative bins to get correct bin numbers (ascending bin numbers for descending values)
    low_bins = low_bins[::-1]

    high_hist, high_bins = np.histogram(lstHigh, bins=10)

    # Binns from Standard Deviations - Did not improve - removed
    # Binns from Percentile - Did not improve - removed

    for i in range(len(lstGE)):

        if lstGE[i] <= fNormalRangeStart:
            sNewGE_Low = sNewGE_Low + str(np.digitize([lstGE[i]], low_bins)[0] + 1) + ','

        else:
            sNewGE_Low = sNewGE_Low + 'N,'

        if lstGE[i] >= fNormalRangeEnd:
            sNewGE_High = sNewGE_High + str(np.digitize([lstGE[i]], high_bins)[0] + 1) + ','

        else:
            sNewGE_High = sNewGE_High + 'N,'

    # N and ','
    if set(sNewGE_Low) == set(['N', ',']):
        sNewGE_Low = ""

    elif len(set(sNewGE_Low)) == 2:
        sNewGE_Low = ""

    else:
        sNewGE_Low = sNewGE_Low[0:-1]

    if set(sNewGE_High) == set(['N', ',']):
        sNewGE_High = ""

    elif len(set(sNewGE_High)) == 2:
        print "Same Count: ", set(sNewGE_High)
        sNewGE_High = ""

    else:
        sNewGE_High = sNewGE_High[0:-1]

    return {0: sNewGE_Low, 1: sNewGE_High}


#####################################################################################################
def scale_expression_values():
    print "input files"
    print "1: Read GE file, 2: Write Discritized file"
    fMETDataFile = open(sys.argv[1], 'r')
    # fMETDataFileV2 = open(sys.argv[2]+'-V2.csv', 'w')
    fMETDataFileV3 = open(sys.argv[2] + '-V3.csv', 'w')

    # Writting the column names back to output file
    col_names = fMETDataFile.readline()
    # fMETDataFileV2.writelines(col_names)
    fMETDataFileV3.writelines(col_names)

    for sLine in fMETDataFile:

        sFields = (sLine.strip(' \t\n')).split(',')
        sScaledGE = sFields[0] + ','

        # Rounding - Did not work removed
        # Bin GE levels

        # V2 - Encode both positive and negative expression values same way
        '''
        binned_v2 = bin_expression_v2_std(sFields[1:len(sFields)])
        if binned_v2 != "":
            sScaledGE = sScaledGE + binned_v2
            fMETDataFileV2.writelines(sScaledGE + '\n')
        '''

        ####################################################################
        # V3 - Encode both positive and negative expression values separately
        # FINAL ENCODING USED IN THE PAPER

        dictNewGE = bin_expression_v3_std(sFields[1:len(sFields)])
        if dictNewGE[0] != "":
            sScaledGE = sFields[0] + "_LOW," + dictNewGE[0]
            fMETDataFileV3.writelines(sScaledGE + '\n')

        if dictNewGE[1] != "":
            sScaledGE = sFields[0] + "_HIGH," + dictNewGE[1]
            fMETDataFileV3.writelines(sScaledGE + '\n')

    fMETDataFile.close()
    # fMETDataFileV2.close()
    fMETDataFileV3.close()


if __name__ == '__main__':
    sys.exit(scale_expression_values())
