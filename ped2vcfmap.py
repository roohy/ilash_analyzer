import numpy as np 
import gzip
import sys
from scipy import stats

dt = np.dtype('U1') 
translate = True
header_list = ['#CHROM',  'POS'   ,  'ID'  ,    'REF',     'ALT' , 'QUAL','FILTER',  'INFO', 'FORMAT']
row_list = ['A',  'G'   , '.' ,'PASS','.' ,'GT']

def map_reader(mapAddr):
    map_data =[]
    with open(mapAddr,'r') as mapfile:
        for line in mapfile:
            data = line.strip().split()
            map_data.append(data)
    return map_data

def line_counter(pedAddr):
    count = 0
    with open(pedAddr) as pedfile:
        for line in pedfile:
            count += 1 
    return count

def translator(dna_mat):
    for i in range(dna_mat.shape[0]):
        stat = stats.itemfreq(dna_mat[i,:])
        if stat.shape[0] < 2:
            dna_mat[i,:] = 1
            continue
        else:
            first_ind = 
            if stat[0,1]>stat[1,1]:


if __name__ == "__main__":
    pedaddr = sys.argv[1]
    mapaddr = sys.argv[2]
    outputaddr = sys.argv[3]
    
    map_data = map_reader(mapaddr)
    line_count = line_counter(pedaddr)

    dna_data = np.zeros((len(map_data)*2,line_count),dtype=dt)
    counter = 0 
    with open(outputaddr+'.vcf','wt') as outputfile:
        outputfile.write('##fileformat=VCFv4.1\n##source=pseq\n##FILTER=<ID=PASS,Description="Passed variant FILTERs">\n')
        outputfile.write("\t".join(header_list))
        with open(pedaddr,'r') as pedfile:
            for line in pedfile:
                data = line.strip().split()
                outputfile.write("\t"+data[1])
                dna_data[:,counter] = data[6:]
                counter += 1
            outputfile.write('\n')
        
        with open(outputaddr+'.map','w') as mapoutputfile:
            for i in range(len(map_data)):
                outputfile.write('chr'+map_data[i][0]+'\t'+map_data[i][3]+'\t'+map_data[i][1]+'\t'+('\t'.join(row_list)) )
                mapoutputfile.write('chr'+map_data[i][0]+'\t'+map_data[i][3]+'\t.\t'+map_data[i][2]+'\n')
                for j in range(line_count):
                    outputfile.write('\t'+dna_data[2*i,j]+'|'+dna_data[(2*i)+1,j])
                outputfile.write('\n')


