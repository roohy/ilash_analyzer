from os import name
import sys
import numpy as np 

def load_map_data(map_addr,gen_pos=False):
    map_data = np.loadtxt(map_addr, skiprows=0,
                          dtype={'names': ['chrom', 'RSID', 'gen_dist', 'position'],
                                 'formats': ['i4', 'U25', 'f4', 'i4']}) #TODO:Change back to S10
    if gen_pos:
        pos_dic = {}
        for i in range(len(map_data)):
            pos_dic[map_data[i][3]] = i
        return map_data,pos_dic
    else:
        return map_data

def make_filter(map_addr,new_map_addr):
    map_data,pos_dic = load_map_data(map_addr,gen_pos=True)
    new_map_data = load_map_data(new_map_addr)
    filter = np.zeros((new_map_data.shape[0]),dtype=np.int)
    for index,item in enumerate(new_map_data):
        filter[index] = pos_dic[item[3]]
    filter = 2*filter
    filter = np.vstack((filter,filter+1)).reshape((-1,),order='F' )
    return filter,map_data.shape[0]
    # index = 0 
    
    # for nindex,item in enumerate(new_map_data):
    #     while map_data[index][3] < item[3]:
    #         index += 1
    #     if map_data[index][3] == item[3]:
    #         filter += index
    #     else:
    #         print('Error in map file - mismatch')
    # return np.array(filter)
def main(ped_addr,map_addr,new_map_addr,output_addr):
    filter,dim = make_filter(map_addr,new_map_addr)
    genotype_data = np.zeros((2*dim),dtype='U1')
    with open(ped_addr,'r') as ped_file:
        with open(output_addr,'w') as output_file:
            for line in ped_file:
                data = line.strip().split()
                output_file.write(' '.join(['gda']+data[1:6])+' ')
                genotype_data[:] = data[6:]
                output_file.write(' '.join(genotype_data[filter])+'\n')

if __name__ == '__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
