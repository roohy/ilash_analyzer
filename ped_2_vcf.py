import sys,os
import numpy as np
from reader import load_map_data

lines = ['##fileformat=VCFv4.2',
            '##fileDate=20200429',
            '##source=Roohyv2.00',
            '##contig=<ID=1,length=247189074>',
            '##INFO=<ID=PR,Number=0,Type=Flag,Description="Provisional reference allele, may not be based on real reference genome">',
            '##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">']
fields = ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT']

if __name__ == '__main__':
    pedAddr = sys.argv[1]
    mapAddr = sys.argv[2]
    vcfAddr = sys.argv[3]
    sampleCount = int(sys.argv[4])
    plinkFlag = int(sys.argv[5])
    mapData,posDict = load_map_data(mapAddr)
    IDList = []
    SNPCount = len(mapData)
    haps = np.zeros((SNPCount,sampleCount),dtype=np.dtype('U3'))
    
    with open(pedAddr,'r') as pedFile:
        for i in range(sampleCount):
            sample = pedFile.readline()
            data = sample.strip().split()
            IDList.append(data[1])
            if plinkFlag == 1:
                for j in range(len(data[6:])):
                    if data[6+j] == '2':
                        data[6+j] = '0'
            for j in range(SNPCount):
                haps[j,i] = data[6+(j*2)]+'|'+data[7+(j*2)]
    with open(vcfAddr,'w') as vcfFile:
        vcfFile.write('\n'.join(lines)+'\n')
        vcfFile.write('\t'.join(fields+IDList)+'\n')
        for i in range(SNPCount):
            vcfFile.write('\t'.join([str(mapData[i][0]),str(mapData[i][3]),
                mapData[i][1].decode('UTF-8'),'C','A','.','.','PR','GT'])+'\t')
            vcfFile.write('\t'.join(haps[i,:])+'\n')
    
        

