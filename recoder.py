import sys


if __name__ == '__main__':
    with open(sys.argv[1],'r') as input_file:
        with open(sys.argv[2],'w') as output_file:
            for line in input_file:
                data = line.strip().split()
                output_file.write(' '.join(data[:6])+' ')
                data = data[6:]
                for i in range(len(data)):
                    if data[i] == '0':
                        data[i] = '1'
                    else:
                        data[i] = '2'
                output_file.write(' '.join(data)+'\n')

                