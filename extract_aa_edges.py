import os,sys

suffix='_abc.edgelist'

if __name__ == '__main__':
    aaFamaddr = sys.argv[1]
    directoryaddr = sys.argv[2]
    outputSuf = sys.argv[3]
    aaFam = set()
    with open(aaFamaddr) as aaFamFile:
        for line in aaFamFile:
            ID = line.strip()
            aaFam.add(ID)
    with open(os.path.join(directoryaddr,'info_file')) as infoFile:
        for line in infoFile:
            number = line.strip().split()[0]
            folderAddr = os.path.join(directoryaddr,str(number))
            with open(os.path.join(folderAddr,suffix)) as graphFile:
                with open(os.path.join(folderAddr,suffix+outputSuf),'w') as outGraphFile:
                    for line in graphFile:
                        data = line.strip().split()
                        if data[0][:-2] in aaFam and data[1][:-2] in aaFam:
                            outGraphFile.write(line.strip()+'\n')