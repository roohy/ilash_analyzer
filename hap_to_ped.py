import numpy as np

def load_haps(hapAddr,size,dim,outputAddr):
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
                output.write(haps[2*i,j]+' ')
                output.write(haps[2*i +1,j]+' ')
            output.write(haps[haps.shape[0]-2,haps.shape[1]-1]+' ')
            output.write(haps[haps.shape[0]-1,haps.shape[1]-1]+'\n')