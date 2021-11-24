import sys
import numpy as np

if __name__ == '__main__':
    vcf_addr = sys.argv[1]
    output_addr = sys.argv[2]
    snp_count = int(sys.argv[3])
    
    with open(vcf_addr,'r') as vcf_file:
        with open(output_addr+'.map','w') as map_file:
            line = None
            while True:
                line = vcf_file.readline()
                if line.startswith('#CHROM'):
                    break
            data = line.strip().split()
            
            id_list = data[9:]
            genotype_array = np.zeros((snp_count*2,len(id_list)),dtype='U1')
            genotype_counter = 0
            for line in vcf_file:
                data = line.strip().split()
                map_file.write(f'{data[0]}\t{data[2]}\t0\t{data[1]}\n')
                alleles = [data[3],data[4]]
                data = data[9:]
                for index,call_pair in enumerate(data):
                    calls = call_pair.split('|')
                    genotype_array[2*genotype_counter , index] = alleles[int(calls[0])]
                    genotype_array[1+(2*genotype_counter), index] = alleles[int(calls[1])]
                genotype_counter += 1
    with open(output_addr+'.ped','w') as ped_file:
        for index,id in enumerate(id_list):
            ped_file.write(f'{id} {id} 0 0 0 -9 '+' '.join(genotype_array[:,index])+'\n')

