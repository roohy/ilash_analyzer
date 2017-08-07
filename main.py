import reader,analyzer,config

import matplotlib.pyplot as plt
import numpy as np
import gc

def get_jaccard(cNum):
    meta_data,pos_dic = reader.load_map_data(config.get_map_address(cNum))
    haps,meta = reader.load_hap_data(config.get_hap_address(cNum))
    match_dic,count = reader.load_ilash(config.get_iLash_address(cNum),pos_dic)
    analyzer.add_jaccard_to_dic(match_dic,haps,config.shingler,20,0)
    return match_dic,count

def rewrite(cNum):
    get_jaccard(cNum)
    reader.write_to_csv()


def print_jaccards(addr):
    for i in range(1,23):
        match_dic,count = get_jaccard(i)
        temp_array = np.zeros((count))
        counter = 0
        for ind1,key1 in enumerate(match_dic):
            for ind2,key2 in enumerate(match_dic[key1]):
                temp_array[counter] = match_dic[key1][key2][3]
                counter += 1
        plt.hist(temp_array, normed=True, bins=10)
        plt.ylabel("probability on Chr"+str(i))
        plt.savefig("fig"+str(i)+".png")
        reader.write_to_csv(match_dic,config.get_jacc_address(i))
        gc.collect()



if __name__ == "__main__":
    print "Analyzer starting"
    for i in range(1, 23):
        map_data, pos_dic = reader.load_map_data(config.get_map_address(i))



