import sys
import numpy as np 

def main():
    input_addr = sys.argv[1]
    output_addr = sys.argv[2]
    size = 0
    real_size = 0 
    with open(input_addr,'r') as input_file:
        with open(output_addr,'w') as output_file:
            for line in input_file:
                if line.startswith('#CHROM'):
                    data = line.strip().split()
                    size = 2000 #
                    real_size = (len(data)-9) #in haps TODO: be very careful with this code 
                    ids = [f'{item:05d}' for item in range(1,size+1)]
                    output_file.write('\t'.join(data[:9]+ids)+'\n')
                    break
                else:
                    output_file.write(line.strip()+'\n') 
            step_size = real_size//size
            for line in input_file:
                data = line.strip().split()
                data[2] = data[1]
                genos = [f'{data[9+i]}|{data[10+i]}' for i in range(0,real_size,step_size)]
                output_file.write('\t'.join(data[:9]+genos)+'\n')
                


if __name__ == '__main__':
    main()