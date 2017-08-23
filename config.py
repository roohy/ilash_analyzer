map_data_prefix = "/lfs1/ibd/belbig01/for_jose-luis/PAGEII_Chr"
map_data_suffix = ".phased.filtered.map3"
hap_data_prefix = map_data_prefix
hap_data_suffix = ".phased.filtered.ped"

iLash_directory_prefix_300 = "../results_300/res_300"
iLash_directory_prefix_400 = "../results_400/"
iLash_directory_prefix_500 = "../results_500/"
iLash_directory_prefix_800 = "../results/"
iLash_directory_prefix_1000 = "../results_1000/"

iLash_data_prefix = "res"
iLash_data_suffix = ".r"

germline_data_prefix = "/lfs1/ibd/belbig01/for_jose-luis/GERMLINE_OUT/PAGEII_Chr"
germline_data_suffix = "_3cM.match"


output_data_prefix = '../new_res/chr_'
output_data_suffix = ""

def get_germline_address(cNum):
    return germline_data_prefix+str(cNum)+germline_data_suffix

def get_iLash_address(cNum):
    return iLash_directory_prefix_300+iLash_data_prefix+str(cNum)+iLash_data_suffix

def get_map_address(cNum):
    return map_data_prefix+str(cNum)+map_data_suffix

def get_hap_address(cNum):
    return hap_data_prefix+str(cNum)+hap_data_suffix

def get_jacc_address(cNum):
    return output_data_prefix+str(cNum)+output_data_suffix

def shingler(haps,shingles_size,overlap):
    result = []
    for i in range(shingles_size,len(haps),shingles_size-overlap):
        result.append(''.join(bite for bite in haps[i-shingles_size:i]))
    return result
