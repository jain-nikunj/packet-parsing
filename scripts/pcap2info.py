from collections import defaultdict
import numpy as np
import sys
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
        timeStamp = round(float(timeStamp), 4)

        if destIp:
            if srcIp.split('.')[3] != str(1):
                arr = destIp.split('.')
                if arr[3] != str(1) and arr[2] == str(curSrn + 100):
                    dictTime2Load[timeStamp] += 1

    return dictTime2Load

def get_offered_load(inputFile, curSrn, dx=1):
    '''
    '''
    dictTime2Load = defaultdict(lambda : 0)

    with open(inputFile, 'r') as inFile:
        lines = inFile.readlines()

    for line in lines:
        data = line.lstrip().rstrip().split(' ')
        timeStamp, srcIp, _, destIp = data[1:5]
        timeStamp = round(float(timeStamp), 4)

        if srcIp:
            if destIp.split('.')[3] != str(1):
                arr = srcIp.split('.')
                if arr[3] != str(1) and arr[2] == str(curSrn + 100):
                    dictTime2Load[timeStamp] += 1

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

def plot_log_offered_load(curCounts, name, dx=1):
    '''

    '''
    counts = len(curCounts)
    endPoint = dx * counts
    timeStamps = np.arange(0, endPoint, dx)
    plt.plot(timeStamps, curCounts)
    plt.savefig(name+".png")
    plt.clf()

def main():
    dx, inputFilePcap, outDir = sys.argv[1:4]
    dx = float(dx)

    # INPUT FILENAME IN THE FORMAT srn<num>_<tap0/tr0>.pcap
    curSrn = int(inputFilePcap.split("_")[0].split("srn")[1])

    dictTime2Load = get_offered_load(inputFilePcap, curSrn, dx)
    curCounts = compute_load_per_dx(dictTime2Load, dx)
    plot_log_offered_load(curCounts, outDir + '/offered_srn{}'.format(curSrn), dx)

    dictTime2Load = get_delivered_load(inputFilePcap, curSrn, dx)
    curCounts = compute_load_per_dx(dictTime2Load, dx)
    plot_log_offered_load(curCounts, outDir + '/delivered_srn{}'.format(curSrn), dx)


if __name__ == '__main__':
    main()
