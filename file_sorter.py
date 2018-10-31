import numpy as np
import sys


if __name__ == '__main__':
    input_addr = sys.argv[1]
    output_addr = sys.argv[2]

    with open(input_addr,'r') as input_file:
        with open(output_addr,'w') as output_file:
            for line in input_file:
                data = line.strip().split('\t')
                id1 = data[1][:-2]
                id2 = data[3][:-2]
                
                if id1 < id2:
                    output_file.write(id1+'\t'+id2+'\t'+data[-2]+'\n')
                else:
                    output_file.write(id2+'\t'+id1+'\t'+data[-2]+'\n')

