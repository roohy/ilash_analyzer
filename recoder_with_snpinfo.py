import sys
import numpy as np

if __name__ == '__main__':
    ped_addr = sys.argv[1]
    snpinfo_addr = sys.argv[2]
    output_addr = sys.argv[3]
    alleles = []

    with open(snpinfo_addr,'r') as snpinfo_file:
        for line in snpinfo_file:
            data = line.strip().split()
            alleles.append((data[-2],data[-3]))
