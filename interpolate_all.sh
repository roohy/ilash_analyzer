MAP=/sc/orga/projects/ipm2/Resources/Genetic_Map_GRCh37/



for i in {1..22}
do

#python interpolate_maps.py UKBB_chr${i}.noindel.map ${MAP}genetic_map_GRCh37_chr${i}.txt UKBB_chr${i}.noindel.genetic.map

python interpolate_maps.py  /sc/arion/projects/ipm2/roohy/gda_ibd/genotype_data/shapeit_normalized_phased_gda_chr_${i}.map /sc/arion/projects/ipm2/Resources/Genetic_Map_GRCh37/genetic_map_GRCh37_chr${i}.txt /sc/arion/projects/ipm2/roohy/gda_ibd/genotype_data/shapeit_normalized_phased_gda_chr_${i}_interpolated.map


# awk -v i="${i}" '{print i" "$1" "$3" "$2}' /sc/private/regen/belbig01/gsa_ancestry/ibd_wreference/input/TGP_GSA_chr${i}.interpolated.map > /sc/private/regen/belbig01/gsa_ancestry/ibd_wreference/input/TGP_GSA_chr${i}.interpolated.map2
# mv /sc/private/regen/belbig01/gsa_ancestry/ibd_wreference/input/TGP_GSA_chr${i}.interpolated.map2 /sc/private/regen/belbig01/gsa_ancestry/ibd_wreference/input/TGP_GSA_chr${i}.interpolated.map
done 