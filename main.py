import reader,analyzer,config
import matplotlib as mpl
mpl.use('Agg') #helps with the X server not connected issue.
import matplotlib.pyplot as plt
import numpy as np
import gc


'''def get_jaccard(cNum):
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

def ibd_distro(match_list):
    dic = []
    for ind1, key1 in enumerate(match_list):
            for ind2, key2 in enumerate(match_list[key1]):
                total = 0
                for i in range(len(match_list[key1][key2])):
                    total += (match_list[key1][key2][i][1] - match_list[key1][key2][i][0])/350
                dic.append(total)
    return dic
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

def print_length()'''

if __name__ == "__main__":
    output = open("concord_res",'w')
    for i in range(1, 23):
        print("chrom: "+str(i))
        map_data, pos_dic = reader.load_map_data(config.get_map_address(i))
        match_dic,count = reader.load_ilash(config.get_iLash_address(i),pos_dic)
        germ_dic,germ_count = reader.load_germline(config.get_germline_address(i),pos_dic)
        overlap_count7 = analyzer.simple_concordance(germ_dic,match_dic,map_data,0.7)
        overlap_count1 =analyzer.simple_concordance(germ_dic,match_dic,map_data,1.0)
        output.write(str(i)+'\t'+str(germ_count)+'\t'+str(count)+'\t'+str(overlap_count1)+'\t'+str(overlap_count7)+'\n')

    '''print "Analyzer starting"
    prob_res = []
    for i in range(1, 23):
        
        map_data, pos_dic = reader.load_map_data(config.get_map_address(i))
        match_dic,count = reader.load_ilash(config.get_iLash_address(cNum),pos_dic)
        prob_res.append(ibd_distro(match_dic))
    cPickle.dump(prob_res,"wow")'''





