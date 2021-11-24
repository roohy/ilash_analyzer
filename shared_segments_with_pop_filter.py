import numpy as np
import sys

thresh = 0.98
dt = np.dtype('uint64')

if __name__ == '__main__':
    match_addr = sys.argv[1]
    map_addr = sys.argv[2]
    cluster_file_addr = sys.argv[3]

    cluster = set()
    snp_dict = {}
    counter = 0
    pos = ''

    with open(map_addr,'r') as map_file:
        for line in map_file:
            pos = line.strip(" ").split()[3]
            snp_dict[int(pos)]= counter
            counter +=1
    results = np.zeros((counter),dtype=dt)
    first = 0
    last = 0
    with open(cluster_file_addr,'r') as cluster_file:
        for line in cluster_file:
            id = line.strip()
            cluster.add(id)
    with open(match_addr, 'r') as match_file:
        for line in match_file:
            line = line.strip().split('\t')
            if line[1][:-2] in cluster and line[3][:-2] in cluster:
                if float(line[10]) > thresh:
                    first = snp_dict[int(line[5])]
                    last = snp_dict[int(line[6])]
                    results[first:last] = results[first:last]+1
    for position in snp_dict:
        print position,results[snp_dict[position]]
