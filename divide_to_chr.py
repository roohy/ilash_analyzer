import numpy as np

meta_length = 6

if __name__ == '__main__':
    ped_addr = '/home/rcf-proj/ta/HRS_AsMa/hrs123_qc1all.ped'
    map_addr = '/home/rcf-proj/ta/rshemira/new_hrs231.map'
    base_new_map_addr = '/home/rcf-proj/ta/rshemira/maps/map'
    base_new_ped_addr = '/home/rcf-proj/ta/rshemira/new_peds/ped_'
    chr_length = {}
    current_chr = -1
    current_file = None
    current_counter = 0
    tail = 0 
    with open(map_addr) as map_file:
        for line in map_file:
            data = line.strip().split()
            chr_num = data[0]
            snp_id = data[1]
            gen_dist = data[2]
            snp_number = int(data[3])
            if chr_num != current_chr:
                if current_file is not None:
                    current_file.close()
                    chr_length[current_chr] = (2*tail,2*(tail+current_counter))
                    tail = tail+current_counter
                current_chr = chr_num
                current_counter = 1
                current_file = 1
                #current_file = open(base_new_map_addr+str(current_chr)+'.map','w')
            else:
                current_counter += 1
            #current_file.write("{chr_num}\t{snp_id}\t{gen_dist}\t{snp_number}\n".format(
            #    chr_num=chr_num,snp_id=snp_id,gen_dist=gen_dist,snp_number=snp_number))
    chr_files = {}
    for key in chr_length:
        chr_files[key] = open(base_new_ped_addr+key+'.ped','w')
        
    with open(ped_addr) as ped_file:
        for line in ped_file:
            data = line.strip().split()
            meta = data[:6]
            data = data[6:]
            for key in chr_length:
                chr_files[key].write(' '.join(meta) + ' ')
                chr_files[key].write(' '.join(data[chr_length[key][0]:chr_length[key][1]]) +'\n')
    for key in chr_files:
        chr_files[key].close()


