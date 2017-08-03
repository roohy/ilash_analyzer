import reader,analyzer,config


def get_jaccard(cNum):
    meta_data,pos_dic = reader.load_map_data(config.get_map_address(cNum))
    haps,meta = reader.load_hap_data(config.get_hap_address(cNum))
    match_dic,count = reader.load_ilash(config.get_iLash_address(cNum),pos_dic)
    analyzer.add_jaccard_to_dic(match_dic,haps,config.shingler,20,0)
    return match_dic

if __name__ == "__main__":
    print "Analyzer starting"

    for i in range(1,23):
        map_data,pos_dic = reader.load_map_data(config.get_map_address(i))
