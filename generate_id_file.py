import sys
import re

def split_iter(string):
    return (x.group(0) for x in re.finditer(r"[A-Za-z0-9\-\_']+", string))

if __name__ == '__main__':
    ped_addr = sys.argv[1]

    res_addr = sys.argv[2]

    with open(ped_addr,'r') as peds:
        with open(res_addr,'w') as res_file:
            for line in peds:
                iter = split_iter(line)
                famID = iter.__next__()
                indID = iter.__next__()
                res_file.write(famID+'\t'+indID+'\n')