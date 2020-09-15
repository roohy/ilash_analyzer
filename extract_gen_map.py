import sys
import numpy as np

if __name__ == '__main__':
    posSet = set()
    with open(sys.argv[1]) as SNPList:
        for line in SNPList:
            id = int(line.strip().split()[1])
            posSet.add(id)
    counter =0 
    with open(sys.argv[3],'w') as outputFile:
        with open(sys.argv[2]) as inputFile:
            for line in inputFile:

                data = line.strip().split()
                id = int(data[2])
                if id not in posSet:
                    counter += 1
    print(counter)
                