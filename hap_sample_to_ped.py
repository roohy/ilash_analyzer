from random import sample
from turtle import write
from unittest import result
import numpy as np 
import gzip,sys

def read_sample(sample_addr):
    ids = []
    with open(sample_addr,'r') as sample_file:
        temp = sample_file.readline()
        temp = sample_file.readline()
        for line in sample_file:
            data = line.strip().split()
            ids.append((data[0],data[1]))
    return ids
def read_hap(hap_addr,sample_count,snp_count):
    positions = []
    snp_ids = []
    genotypes = np.zeros((snp_count,sample_count*2),dtype='U1')
    with gzip.open(hap_addr,'rb') as hap_file:
        for index,line in enumerate(hap_file):
            data = line.decode().strip().split()
            snp_ids.append(data[1])
            positions.append(int(data[2]))
            genotypes[index,:] = list(map(lambda x: '1' if x == '0' else '2', data[5:]))
    
    return genotypes,snp_ids,positions
def load_reference_map(genetic_map_addr,chr_num):
    ref_positions = []
    ref_distances = []       
    chr_flag = False 
    chr_num = str(chr_num)
    with gzip.open(genetic_map_addr,'rb') as genmap_file:
        line = genmap_file.readline()
        for line in genmap_file:
            line = line.decode()
            if line.startswith(chr_num):
                if not chr_flag:
                    chr_flag = True
                data = line.strip().split()
                ref_positions.append(int(data[1]))
                ref_distances.append(float(data[3]))
            elif chr_flag:
                break
            
    return ref_distances,ref_positions


# def write_to_file(handle,chrm,id,dist,position):
#     handle.write(f'{chrm} {id} {dist} {position}\n')


def interpolate_map(positions,ids,ref_distances,ref_positions):
    sindex = 0
    result_map = []
    # with open(output_addr,'w') as output_file:
    for mindex,position in enumerate(positions):
        while ref_positions[sindex]<position and sindex<len(ref_positions)-1:
            sindex += 1
        if position == ref_positions[sindex]:
            result_map.append((ids[mindex],ref_distances[sindex],position))
            # write_to_file(output_file,chrm,ids[mindex],ref_distances[sindex],position)
        elif position < ref_positions[sindex]:
            if sindex == 0:
                result_map.append((ids[mindex],ref_distances[0],position))
                # write_to_file(output_file,chrm,ids[mindex],ref_distances[0],position)
            else:
                prevd = ref_distances[sindex-1]
                prevp = ref_positions[sindex-1]
                frac = (position-prevp)/(ref_positions[sindex]-prevp)
                interpolated_d = prevd + (frac*(ref_distances[sindex]-prevd))
                result_map.append((ids[mindex],interpolated_d,position))
                # write_to_file(output_file,chrm,ids[mindex],interpolated_d,position)
        elif sindex == len(ref_positions)-1:
            result_map.append((ids[mindex],ref_distances[sindex],position))
            # write_to_file(output_file,chrm,ids[mindex],ref_distances[-1],position)
    return result_map
def write_ped(ped_addr,genotypes,samples):
    with open(ped_addr,'w') as ped_file:
        for index,item in enumerate(samples):
            ped_file.write(f'{item[0]} {item[1]} 0 0 0 -9 ')
            print(' '.join(genotypes[:,2*index:2*index+2].reshape(-1)),end='\n',file=ped_file)
    

def map_to_file(map_list,file_addr,chrm):
    with open(file_addr,'w') as output_file:
        for item in map_list:
            output_file.write(f'{chrm} {item[0]} {item[1]} {item[2]}\n')
def main():
    input_addr = sys.argv[1]
    genetic_map_addr = sys.argv[2]
    chr_num = int(sys.argv[3])
    snp_count = int(sys.argv[4])
    output_addr = sys.argv[5]
    hap_addr = input_addr+'.haps.gz'
    sample_addr =input_addr+'.sample'

    ids = read_sample(sample_addr)
    sample_count = len(ids)
    genotypes,snp_ids,positions = read_hap(hap_addr,sample_count,snp_count)
    write_ped(output_addr+'.ped',genotypes,ids)
    del genotypes
    ref_distances,ref_positions = load_reference_map(genetic_map_addr,chr_num)
    map_list = interpolate_map(positions,snp_ids,ref_distances,ref_positions)
    map_to_file(map_list,output_addr+'.map',chr_num)

if __name__ == '__main__':
    main()