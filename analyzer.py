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

def write_concordance(ref_dict,dict_list, name_list,map_data,hap_count,dict_size,output_address):
    output = open(output_address,'w')
    covered_length_list = np.zeros((len(name_list)))
    handles = []
    output.write("hap_num_1\thap_num_2\tStart\tend\tlength")
    for item in name_list:
        output.write('\tcovered_by'+item)
        handles.append(None)
    output.write('\n')

    matched_couple = False
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
                    if tkey1 in dict_list[res_ind] and tkey2 in dict_list[res_ind][tkey1]:
                        temp_list = dict_list[res_ind][tkey1][tkey2]
                    elif tkey2 in dict_list[res_ind] and tkey1 in dict_list[res_ind][tkey2]:
                        temp_list = dict_list[res_ind][tkey2][tkey1]
                    
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


