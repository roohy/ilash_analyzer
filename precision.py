import reader
import os,sys


if __name__ == '__main__':
    pedmap_prefix = sys.argv[1]
    ped_suffix = sys.argv[2]
    map_suffix = sys.argv[3]
    match_prefix = sys.argv[4]
    
    lower_boud = int(sys.argv[5])
    higher_boud = int(sys.argv[6])
    for i in range(lower_boud,higher_boud+1):
        print("CHR:"+str(i))
        map_data,pos_dic = reader.load_map_data(pedmap_prefix+str(i)+map_suffix)
        print("MAP LOADED")
        haps,meta = reader.load_hap_data(pedmap_prefix+str(i)+ped_suffix)
        print("PED LOADED")
        outfile = open(match_prefix+str(i)+'_refined','w')
        with open(match_prefix+str(i), 'r') as match_file:
            for line in match_file:
                data = line.strip().split()
                if float(data[10]) < 1:
                    correct_ones = 0
                    false_ones = 0
                    for snps_ind in range(pos_dic[int(data[5])],pos_dic[int(data[6])]):
                        if haps[data[1]][snps_ind] == haps[data[3]][snps_ind]:
                            correct_ones += 1
                        else:
                            false_ones += 1
                    data[10] = correct_ones/(correct_ones+false_ones)
                outfile.write('\t'.join(data)+'\n')
            outfile.close()
        

