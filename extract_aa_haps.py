import sys
import numpy as np

if __name__ == '__main__':
    cols = []
    with open(sys.argv[1]) as IDList:
        for line in IDList:
            id = int(line.strip().split()[0])
            id -= 2
            cols.append(id*2)
            cols.append((id*2)+1)
    with open(sys.argv[3],'w') as outputFile:
        with open(sys.argv[2]) as inputFile:
            for line in inputFile:
                data = line.strip().split()
                data = np.array(data[5:])
                outputFile.write(' '.join(data[cols])+'\n')
                
                