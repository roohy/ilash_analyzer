import os,sys


def main():
    input_addr = sys.argv[1]
    gsa_dir = sys.argv[2]
    gda_dir = sys.argv[3]
    intra_dir = sys.argv[4]

    match_files_addr_list = [(os.path.join(input_addr,f),f) for f in os.listdir(input_addr) if os.path.isfile(os.path.join(input_addr, f)) and f.endswith('.match')]
    for addr_set in match_files_addr_list:
        with open(addr_set[0],'r') as match_file:
            with open(os.path.join(gsa_dir,addr_set[1]),'w') as gsa_out:
                with open(os.path.join(gda_dir,addr_set[1]),'w') as gda_out:
                    with open(os.path.join(intra_dir,addr_set[1]),'w') as intra_out:
                        for line in match_file:
                            line = line.strip()
                            data = line.split()
                            if data[0] != data[2]:
                                intra_out.write(line+'\n')
                            elif data[0] == 'gsa':
                                gsa_out.write(line+'\n')
                            else:
                                gda_out.write(line+'\n')
if __name__ == '__main__':
    main()