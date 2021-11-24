

#Chromosome	Position(bp)	Rate(cM/Mb)	Map(cM)
# chr2	12994	0.339408	0.000000
# chr2	15491	0.336057	0.000848
import sys, os, gzip

def write_to_file(handle,chrm,id,dist,position):
    handle.write(f'{chrm} {id} {dist} {position}\n')
if __name__ == '__main__':
    map_addr = sys.argv[1] #incomplete map file
    genmap_addr = sys.argv[2] #input map file, either the HapMap map or the 1000 Genomes OMNI map
    output_addr = sys.argv[3]
    positions = []
    ids = []
    
    chrm = None
    with open(map_addr,'r') as map_file:
        for line in map_file:
            data = line.strip().split()
            positions.append(int(data[3]))
            ids.append(data[1])
            chrm = data[0]
    map_positions = []
    map_distances = []        
    with open(genmap_addr,'r') as genmap_file:
        line = genmap_file.readline()
        for line in genmap_file:
            data = line.strip().split()
            map_positions.append(int(data[1]))
            map_distances.append(float(data[3]))
    index1 = 0
    index2 = 0
    sindex = 0
    with open(output_addr,'w') as output_file:
        for mindex,position in enumerate(positions):
            while map_positions[sindex]<position and sindex<len(map_positions)-1:
                sindex += 1
            if position == map_positions[sindex]:
                write_to_file(output_file,chrm,ids[mindex],map_distances[sindex],position)
            elif position < map_positions[sindex]:
                if sindex == 0:
                    write_to_file(output_file,chrm,ids[mindex],map_distances[0],position)
                else:
                    prevd = map_distances[sindex-1]
                    prevp = map_positions[sindex-1]
                    frac = (position-prevp)/(map_positions[sindex]-prevp)
                    interpolated_d = prevd + (frac*(map_distances[sindex]-prevd))
                    write_to_file(output_file,chrm,ids[mindex],interpolated_d,position)
            elif sindex == len(map_positions)-1:
                    write_to_file(output_file,chrm,ids[mindex],map_positions[-1],position)
        