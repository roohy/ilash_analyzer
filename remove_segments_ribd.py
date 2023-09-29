import numpy as np
import sys
import gzip 

thresh = 2.8
dt = np.dtype('uint64')

if __name__ == '__main__':
    match_addr = sys.argv[1]
    chr = sys.argv[2]
    remove_addr = sys.argv[3]
    output_addr = sys.argv[4]
    thresh = float(sys.argv[5])

    remove_list = []
    print("Reading Remove List")
    with open(remove_addr) as remove_file:
        for line in remove_file:
            temp_chr = line.strip(" ").split()[0]
            #if temp_chr > chr :
            #    break
            if temp_chr == chr:
                remove_list.append( ( int(line.strip(" ").split()[1]), int(line.strip(" ").split()[2]) ) )
    count = 0
    first = 0
    last = 0
    flagged = False
    print("Removing lines...")
    with gzip.open(match_addr, 'rb') as match_file:
        with gzip.open(output_addr,'wb') as output_file:
            for line in match_file:
                data = line.decode().strip().split('\t')
                first = int(data[5])
                last = int(data[6])
                if float(data[-1]) < thresh:
                    continue
                flagged = False
                for item in remove_list:
                    if first <= item[1] and  item[0] <=last :
                        count += 1
                        flagged = True
                        break
                if not flagged:
                    output_file.write(line)
    print("DONE!")
    print("Total " + str(count)+ " tracts removed.")