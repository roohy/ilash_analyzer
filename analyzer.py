import numpy as np
from sklearn.metrics import jaccard_similarity_score


def simple_concordance(match_dic,ref_dic,map_data,threshold):
    matched_couple = False
    id1 = ''
    id2 = ''
    overlap_count = 0
    for ind1,key1 in enumerate(match_dic):
        for ind2,key2 in enumerate(match_dic[key1]):
            for tract in match_dic[key1][key2]:

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
                            if map_data[end][2]-map_data[start][2] > threshold:
                                overlap_count += 1
    return overlap_count

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


