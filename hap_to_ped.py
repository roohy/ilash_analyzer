import numpy as np
import sys

def convert_haps(hapAddr,size,dim,outputAddr):
    print("making the matrix")
    haps = np.zeros((size*2,dim),dtype=np.dtype('uint8'))
    counter= 0
    flag = True
    print("opening the file")
    with open(hapAddr,'r') as file:
        for line in file:
            if flag:
                flag = False
                continue
            haps[:,counter] = np.fromstring(line,dtype=int,sep=' ')
            counter += 1
    print("File is loaded")
    haps[haps == 0] = 2
    with open(outputAddr,'w') as output:
        for i in range(haps.shape[0]//2):
            prepended = '%05d' % i
            output.write('0 ' + prepended + ' 0 0 0 -9 ')
            for j in range((haps.shape[1])-1):
                output.write('{} {} '.format(haps[2*i,j],haps[2*i +1,j]))
            output.write('{} {}\n'.format(haps[2*i,haps.shape[1]-1],haps[2*i+1,haps.shape[1]-1]))

if __name__ == '__main__':
    inputAddr = sys.argv[1]
    size = int(sys.argv[2])
    dim = int(sys.argv[3])
    outputAddr = sys.argv[4]
    convert_haps(inputAddr,size,dim,outputAddr)