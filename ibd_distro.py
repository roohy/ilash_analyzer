import numpy as np
import sys

length_sect

def extract_ibds(ibd_file):
    np.zeros((30))
    for line in ibd_file:
        data = line.strip().split()
        length = np.rint(float(data[10]))
        
