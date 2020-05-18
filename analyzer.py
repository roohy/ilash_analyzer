import numpy as np
from sklearn.metrics import jaccard_similarity_score


def simple_concordance(match_dic,ref_dic,map_data,threshold):
    matched_couple = False
    id1 = ''
    id2 = ''
    overlap_count = 0
    for ind1,key1 in enumerate(match_dic):
        for ind2,key2 in enumerate(match_dic[key1]):
            matched_couple = False
            if key1 in ref_dic and key2 in ref_dic[key1]:
                matched_couple = True
                id1 = key1
                id2 = key2
            elif key2 in ref_dic and key1 in ref_dic[key2]:
                matched_couple = True
                id1 = key2
                id2 = key1
            if matched_couple:
                temp_list = ref_dic[id1][id2]
                if len(ref_dic[id1][id2]) > 1:
                    temp_list.sort(key=lambda x: x[0])
                    
                for tract in match_dic[key1][key2]:
                    for item in temp_list:
                        if item[0] > tract[1]:
                            break
                        if item[1] > tract[0]:
                            start = max(item[0],tract[0])
                            end = min(item[1],tract[1])
                            if map_data[end][2]-map_data[start][2] > threshold:
                                overlap_count += 1
            else:
                pass
    return overlap_count
def individual_comparison(ref_dict,dict_list,map_data,hap_count,dict_size,output_address,rapid_ind=-1,ignore_list=None):
    result = []
    dict_to_travers = hap_count//dict_size
    if hap_count%dict_size == 0 :
        dict_to_travers -= 1 
    for i in range(dict_to_travers+1):
        for key1 in ref_dict[i]:
            if key1+(i*dict_size) > hap_count:
                continue
            for key2 in ref_dict[i][key1]:
                if key2+(i*dict_size) > hap_count:
                    continue
                if ignore_list is not None:
                    if key1 in ignore_list[i] and key2 in ignore_list[i][key1]:
                        print("ehem")
                        continue
                    elif key2 in ignore_list[i] and key1 in ignore_list[i][key2]:
                        print('ehem')
                        continue
                total_pair_length = 0
                temp_res_item = []
                for tract in ref_dict[i][key1][key2]:
                    total_pair_length += map_data[tract[1]][2]-map_data[tract[0]][2]
                temp_res_item.append(total_pair_length)
                for res_ind in range(len(dict_list)):
                    tkey1 = key1+(i*dict_size)
                    tkey2 = key2+(i*dict_size)
                    temp_list = None
                    if rapid_ind != res_ind:
                    
                        if tkey1 in dict_list[res_ind] and tkey2 in dict_list[res_ind][tkey1]:
                            temp_list = dict_list[res_ind][tkey1][tkey2]
                        elif tkey2 in dict_list[res_ind] and tkey1 in dict_list[res_ind][tkey2]:
                            temp_list = dict_list[res_ind][tkey2][tkey1]
                    
                    else:
                        rtkey1 = tkey1//2
                        rtkey2 = tkey2//2
                        if rtkey1 in dict_list[res_ind] and rtkey2 in dict_list[res_ind][rtkey1]:
                            temp_list = dict_list[res_ind][rtkey1][rtkey2]
                        elif rtkey2 in dict_list[res_ind] and rtkey1 in dict_list[res_ind][rtkey2]:
                            temp_list = dict_list[res_ind][rtkey2][rtkey1]
                    total_pair_handle = 0    
                    if temp_list is not None:
                        for tract in temp_list:
                            total_pair_handle += map_data[tract[1]][2]-map_data[tract[0]][2]
                    temp_res_item.append(total_pair_handle)
                result.append(temp_res_item)  
    return result
                
                

def write_concordance(ref_dict,dict_list, name_list,map_data,hap_count,dict_size,output_address,rapid_ind=-1):
    output = open(output_address,'w')
    #covered_length_list = np.zeros((len(name_list)))
    handles = []
    output.write("hap_num_1\thap_num_2\tStart\tend\tlength")
    for item in name_list:
        output.write('\tcovered_by'+item)
        handles.append(None)
    output.write('\n')

    #matched_couple = False
    dict_to_travers = hap_count//dict_size
    if hap_count%dict_size == 0 :
        dict_to_travers -= 1 
    for i in range(dict_to_travers+1):
        for key1 in ref_dict[i]:
            if key1+(i*dict_size) > hap_count:
                continue
            for key2 in ref_dict[i][key1]:
                if key2+(i*dict_size) > hap_count:
                    continue
                for res_ind in range(len(name_list)):
                    tkey1 = key1+(i*dict_size)
                    tkey2 = key2+(i*dict_size)
                    temp_list = None
                    if rapid_ind != res_ind:
                    
                        if tkey1 in dict_list[res_ind] and tkey2 in dict_list[res_ind][tkey1]:
                            temp_list = dict_list[res_ind][tkey1][tkey2]
                        elif tkey2 in dict_list[res_ind] and tkey1 in dict_list[res_ind][tkey2]:
                            temp_list = dict_list[res_ind][tkey2][tkey1]
                    
                    else:
                        rtkey1 = tkey1//2
                        rtkey2 = tkey2//2
                        if rtkey1 in dict_list[res_ind] and rtkey2 in dict_list[res_ind][rtkey1]:
                            temp_list = dict_list[res_ind][rtkey1][rtkey2]
                        elif rtkey2 in dict_list[res_ind] and rtkey1 in dict_list[res_ind][rtkey2]:
                            temp_list = dict_list[res_ind][rtkey2][rtkey1]
                        
                    if temp_list is not None:
                        if len(temp_list) > 1:
                            temp_list.sort(key=lambda x: x[0])
                    handles[res_ind] = temp_list    
                for tract in ref_dict[i][key1][key2]:
                    output.write(str(tkey1)+'\t'+str(tkey2)+'\t'+str(tract[0])+'\t'+str(tract[1])+'\t'+str(map_data[tract[1]][2]-map_data[tract[0]][2]))
                    for handle in handles:
                        if handle is None:
                            output.write('\t0')
                        else:
                            covered = 0.0
                            for item in handle:
                                if item[0] > tract[1]:
                                    break
                                if item[1] > tract[0]:
                                    start = max(item[0],tract[0])
                                    end = min(item[1],tract[1])
                                    covered += (map_data[end][2]-map_data[start][2])
                            output.write('\t'+str(covered))
                    output.write('\n')

        


            





def add_concordance(match_dic,ref_dic,map_data,threshold):
    matched_couple = False
    id1 = ''
    id2 = ''
    overlap_count = 0
    for ind1,key1 in enumerate(match_dic):
        for ind2,key2 in enumerate(match_dic[key1]):
            for tract in match_dic[key1][key2]:
                tract.append([])
                matched_couple = False
                if key1 in ref_dic and key2 in ref_dic[key1]:
                    matched_couple = True
                    id1 = key1
                    id2 = key2
                elif key2 in ref_dic and key1 in ref_dic[key2]:
                    matched_couple = True
                    id1 = key2
                    id2 = key1
                if matched_couple:
                    for item in match_dic[id1][id2]:
                        if item[0] > tract[1]:
                            break
                        if item[1] > tract[0]:
                            start = max(item[0],tract[0])
                            end = min(item[1],tract[1])

                            tract[-1].append(map_data[end][2]-map_data[start][2])
                            if map_data[end][2]-map_data[start][2] > threshold:
                                overlap_count += 1

    return overlap_count


#def jackard_sim(id1,id2,)

def add_jaccard_to_dic(match_dic,hap_data,shingler,shingle_size,overlap):
    for ind1, key1 in enumerate(match_dic):
        for ind2, key2 in enumerate(match_dic[key1]):
            for tract in match_dic[key1][key2]:
                tract.append(jaccard_similarity_score(shingler(hap_data[key1][tract[0]:tract[1]],shingle_size,overlap),shingler(hap_data[key2][tract[0]:tract[1]],shingle_size,overlap)))


def load_check_rapid(hap_data,map_data,pos_dic,input_addr):
    output_addr = './fd'
    prefixes = ['_0','_1']
    count = 0 
    length = 0.0
    with open(input_addr) as tracts_file:
        with open(output_addr,'w') as output_file:
            for line in tracts_file:
                data = line.strip().split()
                start_pos = pos_dic[int(data[3])]
                end_pos = pos_dic[int(data[4])]
                if (hap_data[data[1]+prefixes[0]][start_pos:end_pos] == hap_data[data[2]+prefixes[0]][start_pos:end_pos]).all():
                    
                    continue
                elif (hap_data[data[1]+prefixes[0]][start_pos:end_pos] == hap_data[data[2]+prefixes[1]][start_pos:end_pos]).all():

                    continue
                elif (hap_data[data[1]+prefixes[1]][start_pos:end_pos] == hap_data[data[2]+prefixes[0]][start_pos:end_pos]).all():

                    continue
                elif (hap_data[data[1]+prefixes[1]][start_pos:end_pos] == hap_data[data[2]+prefixes[1]][start_pos:end_pos]).all():
                    continue
                else:
                    count += 1 
                    length += map_data[end_pos][2]-map_data[start_pos][2]
    return count,length

'''
def load_check_rapid(hap_data,map_data,pos_dic,input_addr,output_addr):
    
    prefixes = ['_0','_1']
    count = 0 
    length = 0.0
    scores = np.zeros((4))
    with open(input_addr) as tracts_file:
        with open(output_addr,'w') as output_file:
            for line in tracts_file:
                data = line.strip().split()
                start_pos = pos_dic[int(data[3])]
                end_pos = pos_dic[int(data[4])]
                scores[0] = (hap_data[data[1]+prefixes[0]][start_pos:end_pos] == hap_data[data[2]+prefixes[0]][start_pos:end_pos]).sum()
                scores[1] = (hap_data[data[1]+prefixes[0]][start_pos:end_pos] == hap_data[data[2]+prefixes[1]][start_pos:end_pos]).sum()
                scores[2] = (hap_data[data[1]+prefixes[1]][start_pos:end_pos] == hap_data[data[2]+prefixes[0]][start_pos:end_pos]).sum()
                scores[] = (hap_data[data[1]+prefixes[1]][start_pos:end_pos] == hap_data[data[2]+prefixes[1]][start_pos:end_pos]).sum()

                count += 1 
                length += map_data[end_pos][2]-map_data[start_pos][2]
    return count,length


'''