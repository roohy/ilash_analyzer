
if __name__ == '__main__':
    map_addr = ''
    raw_addr = ''
    new_map_addr = ''

    chr_list = {}
    snp_2_dist = {}
    with open(raw_addr,'r') as raw_file:
        for line in raw_file:
            data = line.strip().split()
            snp_2_dist[data[0]] = data[3]
    counter = 0 
    with open(map_addr,'r') as map_file:
        with open(new_map_addr,'w') as new_map_file:
            for line in map_file:
                data = line.strip().split()
                if data[1] not in snp_2_dist:
                    print(data)
                    print("WOW, again? ")
                    snp_2_dist[data[1]] = 'NA'
                counter += 1 
                new_map_file.write(data[0]+'\t'+
                    data[1]+'\t'+snp_2_dist[data[1]]+'\t'+data[3]+'\n')

    print("COUNTER:"+str(counter))
                #new_map_file.write(data[0]+'\t'+
                #    data[1]+'\t'+chr_list[data[0]][data[3]]+'\t'+data[3]+'\n')