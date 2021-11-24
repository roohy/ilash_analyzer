import numpy as np

dt = np.dtype('uint64')
def load_map_data(map_addr):
    map_data = np.loadtxt(map_addr, skiprows=0,
                          dtype={'names': ['chrom', 'RSID', 'gen_dist', 'position'],
                                 'formats': ['i4', 'S10', 'f4', 'i8']})
    pos_dic = {}
    for item in range(len(map_data)):
        pos_dic[map_data[item][3]] = item
    return map_data, pos_dic

heatmap_list = []
for i in range(1,23):
    map_data,pos_dic = load_map_data('/lfs1/ibd/belbig01/for_jose-luis/PAGEII_Chr'+str(i)+'.phased.filtered.map3')
    tempheatmap = np.zeros((len(map_data)),dtype=dt)
    with open('/lfs1/ibd/belbig01/for_jose-luis/GERMLINE_OUT/PAGEII_Chr'+str(i)+'_3cM.match') as germFile:
        for line in germFile:
            data = line.split()
            temp_start = pos_dic[int(data[5])]
            temp_end = pos_dic[int(data[6])]
            tempheatmap[temp_start:temp_end] = tempheatmap[temp_start:temp_end] + 1     
    heatmap_list.append(tempheatmap)
