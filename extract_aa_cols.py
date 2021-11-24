
import sys


if __name__ == '__main__':
    idSet = set()
    with open(sys.argv[1]) as IDList:
        idLine = IDList.readline()
        idData = idLine.strip().split()
        idData = idData[::2]
        for item in idData:
            idSet.add(item)
    with open(sys.argv[3],'w') as outputFile:
        with open(sys.argv[2]) as inputFile:
            counter = 0
            for line in inputFile:
                data = line.strip().split()
                if data[1] in idSet:
                    outputFile.write(str(counter)+'\n')
                counter += 1
                