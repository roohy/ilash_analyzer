import sys


if __name__ == '__main__':
    matrix_file = sys.argv[1]
    fam_file = sys.argv[2]
    outfile = sys.argv[3]

    fam_dict = {}
    with open(fam_file,'r') as fam_file:
        for line in fam_file:
            data = line.strip().split()
            fam_dict[data[1]] = data[0]
    with open(matrix_file,'r') as matrix:
        with open(outfile,'w') as output:
            for line in matrix:
                data = line.strip().split()
                output.write(fam_dict[data[0]]+'\t'+fam_dict[data[1]]+'\t'+data[2]+'\t'+data[3]+'\n')