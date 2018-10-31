import numpy as np
import sys
import pickle

def read_from_file(address):

    results = {}
    
    with open(address, 'r') as match_file:
        for line in match_file:
            data = line.strip().split('\t')
            if data[1][:-2] in results and data[3][:-2] in results[data[1][:-2]]:
                results[data[1][:-2]][data[3][:-2]][0] += 1
                results[data[1][:-2]][data[3][:-2]][1] += float(data[-2])
                continue
            elif data[3][:-2] in results and data[1][:-2] in results[data[3][:-2]]:
                results[data[3][:-2]][data[1][:-2]][0] += 1
                results[data[3][:-2]][data[1][:-2]][1] += float(data[-2])
                continue
            else:
                temp_item = [1,float(data[-2])]
                if data[1][:-2] in results:
                    results[data[1][:-2]][data[3][:-2]]=temp_item
                    continue
                elif data[3][:-2] in results:
                    results[data[3][:-2]][data[1][:-2]]=temp_item
                    continue
                else:
                    results[data[1][:-2]] = {data[3][:-2]:temp_item}
        print('Chromosome Done!')
    return results

def merge(addr1,addr2):
    dict1 = pickle.load(open(addr1,'rb'))
    dict2 = pickle.load(open(addr2,'rb'))
    for key1 in dict1:
        for key2 in dict1[key1]:
            if key1 in dict2 and key2 in dict2[key1]:
                dict2[key1][key2][0] += dict1[key1][key2][0]
                dict2[key1][key2][1] += dict1[key1][key2][1]
                continue
            elif key2 in dict2 and key1 in dict2[key2]:
                dict2[key2][key1][0] += dict1[key1][key2][0]
                dict2[key2][key1][1] += dict1[key1][key2][1]
                continue
            else:
                if key1 in dict2:
                    dict2[key1][key2] = dict1[key1][key2].copy()
                elif key2 in dict2:
                    dict2[key2][key1] = dict1[key1][key2].copy()
                else:
                    dict2[key1] = {key2:dict1[key1][key2].copy()}
    return dict2
def save_fam(text_addr,results, output_addr):
    
    fam_dict = {}
    with open(text_addr,'r') as fam_file:
        for line in fam_file:
            data = line.strip().split()
            fam_dict[data[1]] = data[0]

    print("Starting to write the results.")
    with open(output_addr,'w') as output_file:
        for key1 in results:
            fam_id = fam_dict[key1]
            for key2 in results[key1]:
                output_file.write(fam_id+'\t'+key1+'\t'+fam_dict[key2]+'\t'+key2+'\t'+str(results[key1][key2][0])+'\t'+str(results[key1][key2][1])+'\n')
    print("Everything done")
    


if __name__ == '__main__':
    mode = sys.argv[1]

    if mode == 'single_chr':
        
        match_addr = sys.argv[2]
        output_addr = sys.argv[3]
        pickle.dump(read_from_file(match_addr),open(output_addr,'wb'))

    elif mode == 'merge':
        dict_addr1 = sys.argv[2]
        dict_addr2 = sys.argv[3]
        output_addr = sys.argv[4]
        result = merge(dict_addr1,dict_addr2)
        pickle.dump(result,open(output_addr,'wb'))
    
    elif mode == 'merge_save':
        dict_addr1 = sys.argv[2]
        dict_addr2 = sys.argv[3]
        fam_addr = sys.argv[4]
        output_addr = sys.argv[5]
        result = merge(dict_addr1,dict_addr2)
        save_fam(fam_addr,result,output_addr)





    
    
                        