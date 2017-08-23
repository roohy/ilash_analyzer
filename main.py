import reader,analyzer,config
import matplotlib as mpl
mpl.use('Agg') #helps with the X server not connected issue.
import matplotlib.pyplot as plt
import numpy as np
import gc

def get_jaccard(cNum):
    meta_data,pos_dic = reader.load_map_data(config.get_map_address(cNum))
    print "map file loaded."
    haps,meta = reader.load_hap_data(config.get_hap_address(cNum))
    print "haps loaded"
    match_dic,count = reader.load_ilash(config.get_iLash_address(cNum),pos_dic)
    print "ilash results loaded"
    analyzer.add_jaccard_to_dic(match_dic,haps,config.shingler,20,0)
    print "jaccard results added"
    return match_dic,count

def rewrite(cNum):
    get_jaccard(cNum)
    reader.write_to_csv()


def print_jaccards(addr):
    for i in range(1,23):
        print "Chr #"+str(i)
        match_dic,count = get_jaccard(i)

        temp_array = np.zeros((count),dtype="float")
        counter = 0
        for ind1,key1 in enumerate(match_dic):
            for ind2,key2 in enumerate(match_dic[key1]):
                for item in match_dic[key1][key2]:
                    temp_array[counter] = item[3]
                    counter += 1
        print "starting to draw the histogram!"
        plt.hist(temp_array, normed=True, bins=12)
        plt.ylabel("probability on Chr"+str(i))
        plt.savefig("fig"+str(i)+".png")
        reader.write_to_csv(match_dic,config.get_jacc_address(i))
        gc.collect()



if __name__ == "__main__":
    print "Analyzer starting"
    for i in range(1, 23):
        map_data, pos_dic = reader.load_map_data(config.get_map_address(i))



