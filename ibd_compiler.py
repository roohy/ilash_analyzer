'''This file simulates IBD for our experiments. We first use HapGen to simulate
the genotype data and get Hap files and genetic distance files (a legend file and a genetic 
distance file). 
'''
import numpy as np

dt = np.dtype('uint8')
def load_meta(legendAddr, distsAddr):
    legend = np.loadtxt(legendAddr, skiprows=1, dtype=
    {'names': ['rsid', 'position', 'a1', 'a2'], 'formats': ['U15', 'i4', 'S1', 'S1']})  # legendFormat

    dists = np.loadtxt(distsAddr, skiprows=1, dtype=
    {'names': ['position', 'crate', 'gmap'], 'formats': ['i4', 'f4', 'f4']})
    dists = [[item[0], item[1], item[2]] for item in dists]
    dists = np.array(dists)
    
    nlegend = [(item[1],item[0]) for item in legend]
    legend = np.array([item[0] for item in nlegend])
    the_map = []
    last_base_pos = dists[0]
    
    for item in nlegend:
        first_inds = np.where(dists[:, 0] >= item[0])[0]
        if len(first_inds) > 0:
            if dists[first_inds[0]][0] == item[0]:
                last_base_pos = dists[first_inds[0]]
                the_map.append([item[1], dists[first_inds[0]][2], item[0] ] )
            else:
                first_ind = first_inds[0]
                guestimate = last_base_pos[2]+( (dists[first_ind][2]-last_base_pos[2])/(dists[first_ind][0]-last_base_pos[0])  )*(item[0]-last_base_pos[0])
                the_map.append([item[1], guestimate, item[0] ])
        else:
            sec_las = the_map[-2]
            last_item = the_map[-1]
            guestimate = last_item[1] + ( ((last_item[1]-sec_las[1])/(last_item[2]-sec_las[2]))*(item[0]-last_item[2]) )
            the_map.append([item[1],guestimate, item[0]])



    return np.array(the_map)


def load_haps(hapAddr,size,dim):
    print("making the matrix")
    haps = np.zeros((size*2,dim),dtype=dt)
    counter= 0
    print("opening the file")
    with open(hapAddr,'r') as file:
        for line in file:
            haps[:,counter] = np.fromstring(line,dtype=int,sep=' ')
            counter += 1
    print("File is loaded")
    return haps

def find_intersections(results, new):
    # results = results[results[:,0].argsort()]
    # for i in range(len(results)-1):
    #     if results[i,0] == results[i,]
    for item in results:
        if new[0]>item[0] and new[0]<item[1]:
            return True
        elif new[1]>item[0] and new[1]<item[1]:
            return True
        elif item[0]>new[0] and item[0]<new[1]:
            return True
        elif item[1]>new[0] and item[1]<new[1]:
            return True
        #if len(np.intersect1d(item, new)):
        #    print "overlap"
        #    return True
    return False
def add_to_dict(res_dic,min_ind,max_ind,coordinates,freeze_dic):
    if min_ind in freeze_dic:
        if find_intersections(freeze_dic[min_ind],coordinates):
            return False
        
    if max_ind in freeze_dic:
        if find_intersections(freeze_dic[max_ind], coordinates):
            return False
    if min_ind in freeze_dic:
        freeze_dic[min_ind].append(coordinates)
    else:
        freeze_dic[min_ind] = [coordinates]

    if max_ind in freeze_dic:
        freeze_dic[max_ind].append(coordinates)
    else:
        freeze_dic[max_ind] = [coordinates]

    if min_ind in res_dic:
        if max_ind in res_dic[min_ind]:
            res_dic[min_ind][max_ind].append(coordinates)
        else:
            res_dic[min_ind][max_ind] = [coordinates]
    else:
        res_dic[min_ind] = {}
        res_dic[min_ind][max_ind] = [coordinates]
    
    return True

def tract_generator_from_dist_poisson_reverse(the_map,tract_dist, hap_count):
    results = {}
    freez_dict = {}
    counter = 0
    found = False
    temp_map =  np.array([[float(item[1]),int(item[2])] for item in the_map])
    remaining = 0 
    for size,count in enumerate(reversed(tract_dist)):
        print(remaining)
        print("SIZE IS : "+str(50-size)+'------- #'+str(count))
        
        remaining = int(count)
        
        while remaining>0:
            print("Remaining:"+str(remaining),end='\r')
            found = False
            
            while not found: #finding one of tracts 
                
                if 50-size < 10:
                    shared_by = np.random.poisson(lam=8,size=None)+2
                elif 50-size < 30:
                    shared_by = np.random.poisson(lam=6,size=None)+2
                else:
                    shared_by = np.random.poisson(lam=5,size=None)+2
                added_tracts = shared_by*(shared_by-1)/2
                if remaining-added_tracts < 0:
                    shared_by = 2
                    added_tracts = 1
                    

                indices = sorted(np.random.choice(hap_count, shared_by,replace=False))
                counter = 0
                while counter<3:
                    counter += 1
                    start_loc = np.random.choice(len(temp_map),1)[0]
                    
                    dest = np.where(temp_map[:,0]-temp_map[start_loc,0] >= 50.0-size)[0]
                    if len(dest) == 0 :
                        continue
                    elif add_to_dict_poisson(results,indices,[start_loc,dest[0]],freez_dict):
                        found = True
                        remaining -= added_tracts
                        break
                    else:
                        continue
    return results
def add_to_dict_poisson(res_dic,indices,coordinates,freeze_dic):
    for item in indices:
        if item in freeze_dic:
            if find_intersections(freeze_dic[item],coordinates):
                return False
    for item in indices:
        if item in freeze_dic:
            freeze_dic[item].append(coordinates)
        else:
            freeze_dic[item] = [coordinates]
    for i in range(len(indices)-1):
        if indices[i] not in res_dic:
            res_dic[indices[i]] = {}
        for j in range(i+1,len(indices)):
            if indices[j] in res_dic[indices[i]]:
                res_dic[indices[i]][indices[j]].append(coordinates)
            else:
                res_dic[indices[i]][indices[j]] = [coordinates]
    
    return True

def tract_generator_from_dist_reverse(the_map,tract_dist, hap_count):
    results = {}
    freez_dict = {}
    counter = 0
    found = False
    temp_map =  np.array([[float(item[1]),int(item[2])] for item in the_map])
    for size,count in enumerate(reversed(tract_dist)):
        print("SIZE IS : "+str(50-size)+'------- #'+str(count))
        for i in range(int(count)):
            found = False
            while not found: #finding one of tracts 
                indexes = np.random.choice(hap_count, 2)
                counter = 0
                min_ind = min(indexes)
                max_ind = max(indexes)
                while counter<3:
                    counter += 1
                    start_loc = np.random.choice(len(temp_map),1)[0]
                    
                    dest = np.where(temp_map[:,0]-temp_map[start_loc,0] >= 50.0-size)[0]
                    if len(dest) == 0 :
                        continue
                    elif add_to_dict(results,min_ind,max_ind,[start_loc,dest[0]],freez_dict):
                        found = True
                        break
                    else:
                        continue
    return results


def HD_ibd_generator(the_map,tract_dist, hap_count):
    results = {}
    freez_dict = {}
    counter = 0
    found = False
    temp_map =  np.array([[float(item[1]),int(item[2])] for item in the_map])
    permutation = np.random.permutation(hap_count)
    head = np.zeros(hap_count/2)
    for size,count in enumerate(reversed(tract_dist)):
        print("SIZE IS : "+str(50-size)+'------- #'+str(count))
        for i in range(int(count)):
            found = False
            for j in range(head.shape[0]):
                if temp_map[-1,0]-temp_map[head[j],0] >= 50-size:
                    results

def tract_generator_from_dist(the_map,tract_dist, hap_count):
    results = {}
    freez_dict = {}
    counter = 0
    found = False
    temp_map =  np.array([[item[1],item[2]] for item in the_map])
    for size,count in enumerate(tract_dist):
        for i in range(count):
            found = False
            while not found: #finding one of tracts 
                indexes = np.random.choice(hap_count, 2)
                counter = 0
                min_ind = min(indexes)
                max_ind = max(indexes)
                while counter<3:
                    start_loc = np.random.choice(len(temp_map),1)[0]
                    
                    dest = np.where(temp_map[:,0]-temp_map[start_loc,0] >= size+3)[0]
                    if len(dest) == 0 :
                        continue
                    elif add_to_dict(results,min_ind,max_ind,[start_loc,dest[0]],freez_dict):
                        found = True
                        break
                    else:
                        continue
    return results

def family_generator(the_map, tract_sizes,hap_count):
    results = {}
    freez_dict = {}
    counter = 0
    found = False
    temp_map =  np.array([[item[1],item[2]] for item in the_map])
    for ind,key in enumerate(tract_sizes):
        for i in range(tract_sizes[key]):
            found = False
            while not found: #finding one of tracts 
                indexes = np.random.choice(hap_count, 2)
                counter = 0
                min_ind = min(indexes)
                max_ind = max(indexes)
                while counter<3:
                    start_loc = np.random.choice(len(temp_map),1)[0]
                    
                    dest = np.where(temp_map[:,0]-temp_map[start_loc,0] >= key)[0]
                    if len(dest) == 0 :
                        continue
                    elif add_to_dict(results,min_ind,max_ind,[start_loc,dest[0]],freez_dict):
                        found = True
                        break
                    else:
                        continue
    return results

def make_related(relations, haps):
    for ind,p1 in enumerate(relations):
        for ind2,p2 in enumerate(relations[p1]):
            for item in relations[p1][p2]:
                haps[p2,item[0]:item[1]] = haps[p1,item[0]:item[1]]

def save_map(chr, the_map, file_name):
    with open(file_name,'w') as output:
        for item in the_map:
            output.write(str(chr)+'\t'+item[0]+'\t'+str(item[1])+'\t'+str(item[2])+'\n')

def save_hap(data,file_name):
    with open(file_name,'w') as output:
        for i in range(data.shape[0]//2):
            prepended = '%05d' % i
            output.write('0 ' + prepended + ' 0 0 0 -9 ')
            for j in range((data.shape[1])-1):
                output.write(str(int(data[2*i,j]))+' ')
                output.write(str(int(data[2*i +1,j]))+' ')
            output.write(str(int(data[data.shape[0]-2,data.shape[1]-1]))+' ')
            output.write(str(int(data[data.shape[0]-1,data.shape[1]-1]))+'\n')
    

def load_ilash_for_power(file_name,pos_dic,min_length=1.0,min_acc=0.0,mode='normal'):
    
    count = 0
    match_list = {}
    total_length = 0
    flag = False
    with open(file_name) as iLash:
        for line in iLash:
            data = line.split('\t')
            flag = False
            temp_item = [pos_dic[int(data[5])], pos_dic[int(data[6])],float(data[-2]),float(data[-1])]
            if temp_item[2] < min_length or temp_item[3] < min_acc:
                continue
            count += 1
            total_length += temp_item[2]
                
            if mode == 'individual':
                data[1] = int(data[1][:-2])
                data[3] = int(data[3][:-2])
            else:
                data[1] = int(data[1][:-2])*2 + int(data[1][-1])
                data[3] = int(data[3][:-2])*2 + int(data[3][-1])
            
            if data[1] in match_list:
                if data[3] in match_list[data[1]]:
                    flag = True
                    match_list[data[1]][data[3]].append(temp_item)
                    continue

            if (not flag) and data[3] in match_list:
                if data[1] in match_list[data[3]]:
                    flag = True
                    match_list[data[3]][data[1]].append(temp_item)
                    continue
            if not flag:
                if data[1] in match_list:
                    match_list[data[1]][data[3]] = [temp_item]
                    continue
                elif data[3] in match_list:
                    match_list[data[3]][data[1]] = [temp_item]
                    continue
                else:
                    match_list[data[1]] = {}
                    match_list[data[1]][data[3]] = [temp_item]

    return match_list,count,total_length

def load_beagle_for_power(addr,pos_dic,map_data, min_length=2.75,diploid=True):
    count = 0 
    flag = False
    total_length = 0
    match_list = {}
    with open(addr) as beagleIBD:
        for line in beagleIBD:
            flag = False
            data = line.strip().split()
            start_dist = map_data[pos_dic[int(data[5])]][2]
            end_dist = map_data[pos_dic[int(data[6])]][2]
            genetic_dist = end_dist-start_dist
            if genetic_dist < min_length:
                continue
            id1 = int(data[0][2:])
            id2 = int(data[2][2:])
            if not diploid:
                sign1 = 0 if data[1] == 1 else 1
                sign2 = 0 if data[3] == 1 else 1
                id1 = id1*2 + sign1
                id2 = id2*2 + sign2
            temp_item = [pos_dic[int(data[5])],pos_dic[int(data[6])],genetic_dist]
            count += 1 
            total_length += genetic_dist
            if id1 in match_list:
                if id2 in match_list[id1]:
                    flag = True
                    match_list[id1][id2].append(temp_item)
            if (not flag) and id2 in match_list:
                if id1 in match_list[id2]:
                    match_list[id2][id1].append(temp_item)
            if not flag:
                if id1 in match_list:
                    match_list[id1][id2] = [temp_item]
                elif id2 in match_list:
                    match_list[id2][id1] = [temp_item]
                else:
                    match_list[id1] = {}
                    match_list[id1][id2] = [temp_item]
    return match_list,count,total_length


def load_ribd_for_power(file_name,pos_dic,min_length=1.0,mode='normal'):
    
    count = 0
    match_list = {}
    total_length = 0
    flag = False
    with open(file_name) as ribdFile:
        for line in ribdFile:
            data = line.split('\t')
            flag = False
            temp_item = [pos_dic[int(data[5])], pos_dic[int(data[6])],float(data[-1])]
            if temp_item[2] < min_length:
                continue
            count += 1
            total_length += temp_item[2]
            if mode == 'individual':
                data[1] = int(data[0])
                data[3] = int(data[2])
            else:
                data[1] = int(data[0])*2 + int(data[1])-1
                data[3] = int(data[2])*2 + int(data[3])-1
            
            if data[1] in match_list:
                if data[3] in match_list[data[1]]:
                    flag = True
                    match_list[data[1]][data[3]].append(temp_item)
                    continue

            if (not flag) and data[3] in match_list:
                if data[1] in match_list[data[3]]:
                    flag = True
                    match_list[data[3]][data[1]].append(temp_item)
                    continue
            if not flag:
                if data[1] in match_list:
                    match_list[data[1]][data[3]] = [temp_item]
                    continue
                elif data[3] in match_list:
                    match_list[data[3]][data[1]] = [temp_item]
                    continue
                else:
                    match_list[data[1]] = {}
                    match_list[data[1]][data[3]] = [temp_item]

    return match_list,count,total_length

def load_germline_for_power(addr,pos_dic, min_length=1.0,mode='normal'):
    count = 0
    flag = False
    total_length = 0
    match_list = {}
    with open(addr) as germFile:
        for line in germFile:
            flag = False
            data = line.split()
            id1 = id2 = None
            
                
            if mode == 'individual':
                id1 = int(data[1][:-2]) 
                id2 = int(data[3][:-2]) 
            else:
                if data[1][-1] == '1':
                    sign = '1'
                else:
                    sign = '0'
                if data[3][-1] == '1':
                    sign2 = '1'
                else:
                    sign2 = '0'
                id1 = 2*int(data[1][:-2]) + int(sign)
                id2 = 2*int(data[3][:-2]) + int(sign2)
            temp_item = [pos_dic[int(data[5])], pos_dic[int(data[6])],float(data[10])]
            if temp_item[2] < min_length:
                continue
            count += 1
            total_length += temp_item[2]
            if id1 in match_list:
                if id2 in match_list[id1]:
                    flag = True
                    match_list[id1][id2].append(temp_item)

            if (not flag) and id2 in match_list:
                if id1 in match_list[id2]:
                    flag = True
                    match_list[id2][id1].append(temp_item)
            if not flag:
                if id1 in match_list:
                    match_list[id1][id2] = [temp_item]
                elif id2 in match_list:
                    match_list[id2][id1] = [temp_item]
                else:
                    match_list[id1] = {}
                    match_list[id1][id2] = [temp_item]

    return match_list,count,total_length

def load_rapid_for_power(addr,map_data,pos_dic, min_length):
    count = 0
    total_length = 0
    match_dic = {}
    with open(addr) as results:
        for line in results:
            flag = False
            data = line.strip().split()
            id1 = int(data[1])
            id2 = int(data[2])
            length = map_data[pos_dic[int(data[4])]][2]-map_data[pos_dic[int(data[3])]][2]
            temp_item = [pos_dic[int(data[3])],pos_dic[int(data[4])], length]
            if length < min_length:
                continue
            count += 1
            total_length += length
            if id1 in match_dic:
                if id2 in match_dic[id1]:
                    
                    match_dic[id1][id2].append(temp_item)
                    continue
            if id2 in match_dic:
                if id1 in match_dic[id2]:
                    match_dic[id2][id1].append(temp_item)
                    continue
            if id1 in match_dic:
                match_dic[id1][id2] = [temp_item]
            elif id2 in match_dic:
                match_dic[id2][id1] = [temp_item]
            else:
                match_dic[id1] = {}
                match_dic[id1][id2] = [temp_item]

    return match_dic,count,total_length

def load_ilash_length(address, pos_dic):
    count = 0
    total_length = 0
    with open(address) as iLash:
        for line in iLash:
            data = line.split('\t')
            flag = False
            temp_item = float(data[-2])
            count += 1
            total_length += temp_item
    return count,total_length
def load_ribd_length(address, pos_dic):
    count = 0
    total_length = 0
    with open(address) as ribdFile:
        for line in ribdFile:
            data = line.split('\t')
            flag = False
            temp_item = float(data[-1])
            count += 1
            total_length += temp_item
    return count,total_length

def load_germline_length(address,pos_dic):
    count = 0
    total_length = 0
    with open(address) as germFile:
        for line in germFile:
            
            data = line.split()
            
            temp_item =float(data[10])
            count += 1
            total_length += temp_item
    return count,total_length

def load_rapid_length(address,pos_dic,map_data):
    count = 0 
    total_length = 0 
    with open(address) as inputfile:
        for line in inputfile:
            data = line.split()

            length = map_data[pos_dic[int(data[4])]][2]-map_data[pos_dic[int(data[3])]][2]
            count += 1 
            total_length += length
    return count,total_length

def load_beagle_length(addr,pos_dic,map_data, min_length=2.75):
    count = 0
    total_length = 0
    with open(addr) as beagleIBD:
        for line in beagleIBD:
            data = line.strip().split()
            start_dist = map_data[pos_dic[int(data[5])]][2]
            end_dist = map_data[pos_dic[int(data[6])]][2]
            genetic_dist = end_dist-start_dist
            if genetic_dist < min_length:
                continue
            count += 1 
            total_length += genetic_dist
    return count,total_length
    
#dictSize should be in haps since the input is haplotype based. 
def change_hap_dict(refDictList,dictSize,indCount):
    hapCount = 2*indCount
    dictToTraverse = hapCount//dictSize
    if hapCount%dictSize == 0 :
        dictToTraverse -= 1 
    resultDictList = []
    for i in range(dictToTraverse+1):
        tempDict = {}
        for key1 in refDictList[i]:
            if key1+(i*dictSize) > hapCount:
                continue
            for key2 in refDictList[i][key1]:
                if key2+(i*dictSize) > hapCount:
                    continue
                tempTractList = refDictList[i][key1][key2]
                tkey1 = key1//2
                tkey2 = key2//2
                if tkey1 not in tempDict and tkey2 not in tempDict:
                    tempDict[tkey1] = {tkey2:tempTractList}
                elif tkey2 not in tempDict:
                    if tkey2 in tempDict[tkey1]:
                        tempDict[tkey1][tkey2] += tempTractList
                    else:
                        tempDict[tkey1][tkey2] = tempTractList
                elif tkey1 not in tempDict:
                    if tkey1 in tempDict[tkey2]:
                        tempDict[tkey2][tkey1] += tempTractList
                    else:
                        tempDict[tkey2][tkey1] = tempTractList
                else:
                    if tkey2 in tempDict[tkey1]:
                        tempDict[tkey1][tkey2] += tempTractList
                    elif tkey1 in tempDict[tkey2]:
                        tempDict[tkey2][tkey1] += tempTractList 
                    else:
                        tempDict[tkey1][tkey2] = tempTractList
        resultDictList.append(tempDict)
    return resultDictList
                




def check_sim_ibd(fam_dic,match_dic):
    
    for ind1,p1 in enumerate(fam_dic):
        for ind2,p2 in enumerate(fam_dic[p1]):
            if p1 in match_dic:
                if p2 in match_dic[p1]:
                    pass




                


