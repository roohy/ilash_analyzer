import numpy as np
import sys

list_of_addrs = []
list_of_files = []
list_of_lines = []
output_file = None

def print_line(output_data):
    output_file.write(output_data[0]+'\t'+output_data[1]+'\t'+str(output_data[2])+'\t'+ str(output_data[3])+'\n')


def extract_min():
    global list_of_lines
    if len(list_of_files) == 0:
        return None
    minimum = np.argmin(list_of_lines)
    result = list_of_lines[minimum]
    line = list_of_files[minimum].readline()
    if not line:
        del list_of_files[minimum]
        list_of_lines = list_of_lines.tolist()
        del list_of_lines[minimum]
        list_of_lines = np.array(list_of_lines)
    else:
        list_of_lines[minimum] = line
    return result

if __name__ == '__main__':
    file_list_addr = sys.argv[1]
    output_addr = sys.argv[2]
    output_file = open(output_addr,'w')
    with open(file_list_addr,'r') as file_list_file:
        for line in file_list_file:
            list_of_addrs.append(line.strip())
    for addr in list_of_addrs:
        list_of_files.append(open(addr,'r'))
    for chunk in list_of_files:
        list_of_lines.append(chunk.readline())
    list_of_lines = np.array(list_of_lines)
    current_line = extract_min()
    current_data = current_line.strip().split()
    current_data[2] = float(current_data)
    if len(current_data) == 3:
        current_data.append(1)
    else:
        current_data[3] = int(current_data[3])
    
    next_line = extract_min()

    while next_line is not None:
        next_data = next_line.strip().split()
        if next_data[0] == current_data[0] and next_data[1] == current_data[1]:
            current_data[2] += float(next_data[2])
            if len(next_data) == 3:
                current_data[3] += 1 
            else:
                current_data[3] += int(next_data[3])
        else:
            print_line(current_data)
            current_data = next_data
            if len(current_data) == 3:
                current_data.append(1)
            else:
                current_data[3] = int(current_data[3])
            current_data[2] = float(current_data[2])
            
        next_line = extract_min()
    print_line(current_data)
    output_file.close()
    

