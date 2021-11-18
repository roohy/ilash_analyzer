import sys
import numpy as np

def findHead(genData,index,position):
    while index < genData.shape[0] and genData[index][1] < position:
        index += 1
    result = (position-genData[index-1][1])* (genData[index-1][2]-genData[index-2][2])/(genData[index-1][1]-genData[index-2][1])
    return result+genData[index-1][2],index-1

if __name__ == '__main__':
    genMapAddr = sys.argv[1]
    queryAddr = sys.argv[2]
    outputAddr = sys.argv[3]
    queryData = np.loadtxt(queryAddr,dtype={'names': ['RSID' ,'position'],
                                 'formats': [ 'S20' ,'i8']})
    chr = '6'
    '''queryDict = {}
    for i in range(queryData.shape[0]):
        queryDict[queryData[i][1]] = i'''
    genData =np.loadtxt(genMapAddr,dtype={'names': ['RSID', 'position' ,'gen_dist' ],
                                 'formats': ['S20' , 'i8' , 'f8']})
    genDict = {}
    for i in range(genData.shape[0]):
        genDict[genData[i][1]] = i
    lastIndex = 0 
    tempDist = 0
    with open(outputAddr,'w') as outputFile:
        for queryItem in queryData:
            if queryItem[1] in genDict:
                tempDist = genData[genDict[queryItem[1]]][2]
                lastIndex = genDict[queryItem[1]]
            else:
                tempDist,lastIndex = findHead(genData,lastIndex,queryItem[1])
            outputFile.write(' '.join([chr,str(queryItem[0]),str(tempDist),str(queryItem[1])])+'\n')
        #outputFile.write(' '.)
