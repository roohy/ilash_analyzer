import sys,os

def write_file(links,output_addr):
    count = 0
    with open(output_addr,'w') as output_file:
        for id1 in links:
            for id2 in links[id1]:
                count += 1
                if links[id1][id2] >= 6.0:
                    output_file.write(f'{id1}\t{id2}\t{links[id1][id2]}\n')
    print(f'Total connection count is {count}')

def make_links(input_addr):
    links = {}
    match_files_addr_list = [os.path.join(input_addr,f) for f in os.listdir(input_addr) if os.path.isfile(os.path.join(input_addr, f)) and f.endswith('.match')]
    for addr in match_files_addr_list:
        with open(addr,'r') as match_file:
            for line in match_file:
                data = line.strip().split()
                id1 = data[1][:-2]
                id2 = data[3][:-2]
                link_length = float(data[-2])
                if id1 in links:
                    if id2 in links[id1]:
                        links[id1][id2] += link_length
                        continue
                    elif id2 not in links:
                        links[id1][id2] = link_length
                        continue
                if id2 in links:
                    if id1 in links[id2]:
                        links[id2][id1] += link_length

                    else:
                        links[id2][id1] = link_length
                else:
                    links[id1] = {}
                    links[id1][id2] = link_length
    return links
def main():
    links = make_links(sys.argv[1])
    write_file(links,sys.argv[2])


if __name__ == '__main__':
    main()
