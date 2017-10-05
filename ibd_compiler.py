import numpy as np


def load_meta(legendAddr, distsAddr):
    legend = np.loadtxt(legendAddr, skiprows=1, dtype=
    {'names': ['rsid', 'position', 'a1', 'a2'], 'formats': ['S15', 'i4', 'S1', 'S1']})  # legendFormat

    dists = np.loadtxt(distsAddr, skiprows=1, dtype=
    {'names': ['position', 'crate', 'gmap'], 'formats': ['i4', 'f4', 'f4']})
    dists = [[item[0], item[1], item[2]] for item in dists]
    dists = np.array(dists)
    nlegend = [(item[1],item[0]) for item in legend]
    nlegend = np.array(nlegend)
    the_map = []
    last_base_pos = 0.000 
    
    for item in nlegend:
        first_inds = np.where(dists[:, 0] >= item[0])[0]
        if len(first_inds) > 0:
            if dists[first_inds[0]][0] == item[0]:
                last_base_pos = dists[first_inds]
                the_map.append([item[1], dists[first_inds[0]][2], item[0] ] )
            else:
                first_ind = first_inds[0]
                guestimate = last_base_pos[2]+( (dists[first_ind][2]-last_base_pos[2])/(dists[first_ind][0]-last_base_pos[0])  )*(item[0]-last_base_pos[0])
                the_map.append([item[1], guestimate, item[0] ])
        else:
            sec_las = the_map[-2]
            last_item = the_map[-1]
            guestimate = last_item[1] + ( ((last_item[1]-sec_las[1])/(last_item[2]-sec_las[2]))*(item[0]-last_item[2]) )



    return np.array(the_map)

def load_haps(hapAddr,size,dim):
    print("making the matrix")
    haps = np.zeros((size*2,dim))
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
        res_dic[min_ind][max_ind] = [coordinates]
    
    return True



def family_generator(the_map, tract_sizes,hap_count):
    results = {}
    freez_dict = {}
    counter = 0
    found = False
    
    for ind,key in enumerate(tract_sizes):
        for i in range(tract_sizes[key]):
            found = False
            while not found: #finding one of tracts 
                indexes = np.random.choice(hap_count, 2)
                counter = 0
                min_ind = min(indexes)
                max_ind = max(indexes)
                while counter<3:
                    start_loc = np.random.choice(len(the_map,1)[0]
                    
                    dest = np.where(the_map[:,1]-the_map[start_loc,1] >= key)[0]
                    if len(dest) == 0 :
                        continue
                    elif add_to_dict(res_dic,min_ind,max_ind,[start_loc,dest],freez_dict):
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
            output.write(str(chr)+'\t'+"\t".join(str(j for j in item))+'\n')

def save_hap(data,file_name):
    with open(file_name,'w') as output:
        for i in range(data.shape[0]/2):
            prepended = '%05d' % i
            file.write('0 ' + prepended + ' 0 0 0 -9 ')
            for j in range((data.shape[1])-1):
                file.write(str(int(data[2*i,j]))+' ')
                file.write(str(int(data[2*i +1,j]))+' ')
            file.write(str(int(data[data.shape[0]-2,data.shape[1]-1]))+' ')
            file.write(str(int(data[data.shape[0]-1,data.shape[1]-1]))+'\n')
    








                


