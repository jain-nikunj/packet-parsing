from collections import defaultdict
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def get_delivered_load(inputFile, curSrn, dx=1):
    '''
    '''
    dictTime2Load = defaultdict(lambda : 0)

    with open(inputFile, 'r') as inFile:
        lines = inFile.readlines()

    for line in lines:
        data = line.lstrip().rstrip().split(' ')
        timeStamp, srcIp, _, destIp = data[1:5]
        byteLen = int(data[6])
        timeStamp = round(float(timeStamp), 4)

        if destIp:
            if srcIp.split('.')[3] != str(1):
                arr = destIp.split('.')
                if arr[3] != str(1) and arr[2] == str(curSrn + 100):
                    dictTime2Load[timeStamp] += byteLen

    return dictTime2Load

def get_offered_load(inputFile, curSrn, dx=1):
    '''
    '''
    dictTime2Load = defaultdict(lambda : 0)

    with open(inputFile, 'r') as inFile:
        lines = inFile.readlines()

    for line in lines:
        data = line.lstrip().rstrip().split(' ')
        data = list(filter(None, data))
        timeStamp, srcIp, _, destIp = data[1:5]
        timeStamp = round(float(timeStamp), 4)
        byteLen = int(data[6])

        if srcIp:
            if destIp.split('.')[3] != str(1):
                arr = srcIp.split('.')
                if arr[3] != str(1) and arr[2] == str(curSrn + 100):
                    dictTime2Load[timeStamp] += byteLen

    return dictTime2Load

def compute_load_per_dx(dictTime2Load, dx=1):
    curX = 0
    curCounts = [0]
    for key in sorted(dictTime2Load.keys()):
        val = dictTime2Load[key]
        if key - curX < dx:
            curCounts[-1] += val
        else:
            curCounts[-1] /= dx
            while key - curX > dx:
                curX += dx
            curCounts.append(val)

    return curCounts

def plot_log_offered_load(curCountArr, priorityArr, name, dx=1):
    '''

    '''
    legs = []
    for i, curCounts in enumerate(curCountArr):
        priority = priorityArr[i]
        counts = len(curCounts)
        endPoint = dx * counts
        timeStamps = np.arange(0, endPoint, dx)
        leg, = plt.plot(timeStamps, curCounts, label=priority)
        legs.append(leg)

    plt.legend(legs, priorityArr)
    plt.ylabel('Bytes / Sec')
    plt.title("Load averaged over dx={}".format(str(dx)))
    plt.savefig(name+".png")
    plt.clf()

def main():
    dx, outDir = sys.argv[1:3]
    inputFileTxts = sys.argv[3:]
    dx = float(dx)
    curCountArr = []
    priorityArr = []

    # INPUT FILENAME IN THE FORMAT srn<num>-*-priority.txt
    for inputFileTxt in inputFileTxts:
            curSrn = int(inputFileTxt.split("-")[0].split("srn")[1])
            priority = inputFileTxt.split("-")[-1].split(".")[0]

            dictTime2Load = get_offered_load(inputFileTxt, curSrn, dx)
            curCounts = compute_load_per_dx(dictTime2Load, dx)
            curCountArr.append(curCounts)
            priorityArr.append(priority)

    plot_log_offered_load(curCountArr, priorityArr,
                          outDir + '/offered_srn{}'.format(curSrn), dx)

if __name__ == '__main__':
    main()
