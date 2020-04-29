import numpy as np
dt = np.dtype('uint8')
def load_map_data(map_addr):
    map_data = np.loadtxt(map_addr, skiprows=0,
                          dtype={'names': ['chrom', 'RSID', 'gen_dist', 'position'],
                                 'formats': ['i4', 'S10', 'f4', 'i4']})
    pos_dic = {}
    for item in range(len(map_data)):
        pos_dic[map_data[item][3]] = item
    return map_data, pos_dic
def fix_map(mapData):
    lastVal = 0
    for i in range(1,len(mapData)):
        if mapData[i-1][2] > mapData[i][2]:
            mapData[i-1][2] = (mapData[i][2]+mapData[i-2][2])/2
        lastVal = mapData[i][2]
    return mapData
def save_map(mapAddr,mapArray):
        with open(mapAddr,'w') as mapFile:
            for mapItem in mapArray:
                mapFile.write('\t'.join([str(item) for item in mapItem])+'\n')
def load_hap_data(hap_addr):
    haps = {}
    meta = {}
    with open(hap_addr) as file:
        for line in file:
            data = line.split()
            temp_hap = np.array(data[6:])
            if data[1] + '_0' in haps:
                print("wow we messed up")
            haps[data[1] + '_0'] = temp_hap[::2]
            haps[data[1] + '_1'] = temp_hap[1::2]
            meta[data[1] + '_0'] = data[0]
            meta[data[1] + '_1'] = data[0]
    return haps,meta

def full_hap_loader_disjoint(base_addr,addr_suffix,count,base_map_addr,map_addr_suffix):
    dna_length = 0
    chr_bounds = {}
    for i in range(1,23):
        map_data = np.loadtxt(base_map_addr+str(i)+map_addr_suffix, skiprows=0,
                              dtype={'names': ['chrom', 'RSID', 'gen_dist', 'position'],
                                     'formats': ['i4', 'S10', 'f4', 'i4']})
        chr_bounds[i] = (dna_length, dna_length + len(map_data))
        dna_length += len(map_data)

    dna_array = np.zeros((count,dna_length*2))
    for i in range(1,23):
        with open(base_addr+str(i)+addr_suffix) as file:
            temp_count = 0
            for line in file:
                data = line.split()
                dna_array[count,chr_bounds[i][0]:chr_bounds[i][1]] = np.array(data[6:]).astype(np.int)
                temp_count += 1
                if temp_count >= count:
                    break
    return dna_array


def load_ilash(addr,pos_dic,min_length=2.0 , min_acc = 0.0):
    count = 0
    match_list = {}

    flag = False

    with open(addr) as iLash:
        for line in iLash:
            data = line.split('\t')
            flag = False
            temp_item = [pos_dic[int(data[5])], pos_dic[int(data[6])],float(data[-2]),float(data[-1])]
            if temp_item[2] < min_length or temp_item[3] < min_acc:
                continue
            count += 1
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



    return match_list,count

def load_germline(addr,pos_dic, min_length=1.0):
    count = 0
    flag = False
    match_list = {}
    with open(addr) as germFile:
        for line in germFile:
            flag = False
            data = line.split()
            if data[1][-1] == '1':
                sign = '1'
            else:
                sign = '0'
            if data[3][-1] == '1':
                sign2 = '1'
            else:
                sign2 = '0'
            id1 = data[1][:-2] + '_' + sign
            id2 = data[3][:-2] + '_' + sign2
            temp_item = [pos_dic[int(data[5])], pos_dic[int(data[6])],float(data[10])]
            if temp_item[2] < min_length:
                continue
            count += 1
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

    return match_list,count


def write_to_csv(match_list,addr):
    file = open(addr,'w')
    for ind1, key1 in enumerate(match_list):
        for ind2, key2 in enumerate(match_list[key1]):
            for item in match_list[key1][key2]:
                file.write(key1+ ',' + key2 + ',' + ','.join(str(i) for i in item)+'\n')

def read_from_csv(addr):
    return np.genfromtxt(addr,delimiter=',')

def load_and_check_ilash(address, pos_dic,haps):
    total = 0
    true = 0
    cmCount = 0
    cmLen = 0
    match_list = {}
    flag = False
    try:
        with open(address) as iLash:
            for line in iLash:
                data = line.split('\t')
                if int(data[3]) < int(data[2]):
                    print("ooops")
                total += pos_dic[int(data[3])] - pos_dic[int(data[2])]
                true += np.sum(haps[data[0]][pos_dic[int(data[2])]:pos_dic[int(data[3])]] == haps[data[1]][pos_dic[int(data[2])]:pos_dic[int(data[3])]])
                cmCount += 1
                cmLen += float(data[-1][:-3])
                flag = False
                if data[0] in match_list:
                    if data[1] in match_list[data[0]]:
                        flag = True
                        handle = match_list[data[0]][data[1]].append([pos_dic[int(data[2])], pos_dic[int(data[3])]])

                if (not flag) and data[1] in match_list:
                    if data[0] in match_list[data[1]]:
                        flag = True
                        handle = match_list[data[1]][data[0]].append([pos_dic[int(data[2])], pos_dic[int(data[3])]])
                if not flag:
                    if data[0] in match_list:
                        match_list[data[0]][data[1]] = [[pos_dic[int(data[2])], pos_dic[int(data[3])]]]
                    elif data[1] in match_list:
                        match_list[data[1]][data[0]] = [[pos_dic[int(data[2])], pos_dic[int(data[3])]]]
                    else:
                        match_list[data[0]] = {}
                        match_list[data[0]][data[1]] = [[pos_dic[int(data[2])], pos_dic[int(data[3])]]]
        count = 0
        for ind1, key1 in enumerate(match_list):
            for ind2, key2 in enumerate(match_list[key1]):
                if len(match_list[key1][key2]) > 1:
                    temp_list = match_list[key1][key2]
                    temp_list.sort(key=lambda x: x[0])
                    for i in range(len(temp_list)):
                        for j in range(i + 1, len(temp_list)):
                            if temp_list[j][0] > temp_list[i][1]:
                                break
                            else:
                                count += 1
        return total, true, cmCount, cmLen, match_list, count
    except:
        print("Not Found")
        return 1, 0, 1, 1, {}, 1