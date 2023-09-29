import numpy as np
import sys

thresh = 0.5
dt = np.dtype('uint64')

def load_map(map_addr):
    map_data = np.loadtxt(map_addr, skiprows=0,
                          dtype={'names': ['chrom', 'RSID', 'gen_dist', 'position'],
                                 'formats': ['i4', 'S10', 'f4', 'i8']})
    pos_dic = {}
    for item in range(len(map_data)):
        pos_dic[map_data[item][3]] = item
    return map_data, pos_dic
def read_depth(ibd_addr,map_data,pos_dic):
    hits = np.zeros(map_data.shape)
    with open(ibd_addr,'r') as match_file:
        for line in match_file:
            data = line.strip().split()
            hits[pos_dic[int(data[5])]:pos_dic[int(data[6])] ] += 1
    return hits
def 

if __name__ == '__main__':
    match_addr = sys.argv[1]
    chr = sys.argv[2]
    remove_addr = sys.argv[3]
    output_addr = sys.argv[4]

    remove_list = []
    print("Reading Remove List")
    with open(remove_addr) as remove_file:
        for line in remove_file:
            temp_chr = line.strip(" ").split()[0]
            #if temp_chr > chr :
            #    break
            if temp_chr == chr:
                remove_list.append( ( int(line.strip(" ").split()[1]), int(line.strip(" ").split()[2]) ) )
    count = 0
    first = 0
    last = 0
    flagged = False
    print("Removing lines...")
    with open(match_addr, 'r') as match_file:
        with open(output_addr,'w') as output_file:
            for line in match_file:
                data = line.strip().split('\t')
                first = int(data[5])
                last = int(data[6])
                flagged = False
                for item in remove_list:
                    if first <= item[1] and  item[0] <=last :
                        count += 1
                        flagged = True
                        break
                if not flagged:
                    output_file.write(line)
    print("DONE!")
    print("Total " + str(count)+ " tracts removed.")