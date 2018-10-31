import numpy as np
import pickle
from ibd_compiler import *




if __name__ == '__main__':
    distro = np.zeros((50))
    with open('./PuertoRican.chr1.match') as ibds:
        for line in ibds:
            length = int(np.rint(float(line.strip().split()[10])))
            if length < 3:
                continue
            if length > 50:
                length = 50
            distro[length-3] += 1 
    normalizer = 12116*12115/2
    scale = 2000*1999/2
    final_distro = (distro/normalizer)*scale
    tract_list = []
    the_map = load_meta('../power_test/HM3_chr1/hapmap3.r2.b36.chr1.legend','../power_test/HM3_chr1/genetic_map_chr1_combined_b36.txt')
    for i in range(20):
        
        ibd_dict = tract_generator_from_dist_poisson_reverse(the_map,final_distro[:-2],2000)
        tract_list.append(ibd_dict)

    pickle.dump(tract_list,open('./tracts_general_small_PR','wb'))
    #haps = load_haps('test.80000.controls.haps',80000,116415)