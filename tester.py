import numpy as np
import os
from timer import ProcessTimer

PED_ADDRESS='ped'
MAP_ADDRESS='map'
OUTPUT_ADDRESS = 'output'
ILASH_ADDR = '/lfs1/ibd/IBD/build/ilash'
BUCKET_COUNT  = 'bucket_count'
PERM_COUNT = 'perm_count'
MIN_LENGTH = 'min_length'
SLICE_LENGTH = 'slice_length'



class TesterBase:
    def __init__(self,directory):
        self.parameters = {}
        self.fileName = ''
        self.directory = directory
        if not os.path.isdir(self.directory):
            os.makedirs(self.directory)
    
    def __iter__(self):
        return self

    def __next__(self):
        return 0
    
    def write_to_file(self):
        with open(self.fileName,'w') as configFile:
            for key in self.parameters:
                configFile.write(key+'  '+str(self.parameters[key])+'\n')
    def run_experiment(self):
        self.write_to_file()
        ptimer = ProcessTimer([ILASH_ADDR,self.fileName])
        ptimer.execute()
        self.measures = ptimer.wait()
        return self.measures



''' 
    FPT(directory,hapfile,mapfile)
    set_break_points(address)
    load_haps(add,size,dim)
    mak_haps()
'''  
class FPTester(TesterBase):
    def __init__(self,directory,hapFileAddress,mapFile,it_count,sampleCounter,snpCounter,pedMode=False):
        super().__init__(directory)
        self.it_count = it_count
        if not pedMode:
            self.haps = FPTester.load_haps(hapFileAddress,sampleCounter,snpCounter)
        else:
            self.haps = ThinnerTester.load_ped(hapFileAddress,sampleCounter,snpCounter)
        self.parameters[MAP_ADDRESS] = mapFile
        self.parameters[MIN_LENGTH] = 3.0
        self.parameters[SLICE_LENGTH] = 3.0
        

    def set_break_points(self,breakListAddress):
        self.breakList = np.load(breakListAddress)
    
    @staticmethod
    def load_haps(hapAddr,size,dim):
        print("making the matrix")
        haps = np.zeros((size*2,dim),dtype=np.dtype('uint8'))
        counter= 0
        flag = True
        print("opening the file")
        with open(hapAddr,'r') as file:
            for line in file:
                if flag:
                    flag = False
                    continue
                haps[:,counter] = np.fromstring(line,dtype=int,sep=' ')
                counter += 1
        print("File is loaded")
        haps[haps == 0] = 2
        return haps

    @staticmethod
    def make_haps(oldHaps,breakList):
        newHaps = np.zeros(oldHaps.shape,dtype=np.dtype('U1'))
        hapCount = newHaps.shape[0]
        for breakLine in breakList:
            perms = np.random.permutation(hapCount)
            counter = 0
            for i in range(hapCount):
                newHaps[i,breakLine[0]:breakLine[1]] = oldHaps[perms[i],breakLine[0]:breakLine[1]]
        return newHaps
    
    @staticmethod
    def save_haps(haps,fileName):
        with open(fileName,'w') as output:
            for i in range(haps.shape[0]//2):
                prepended = '%05d' % i
                output.write('0 ' + prepended + ' 0 0 0 -9 ')
                for j in range((haps.shape[1])-1):
                    output.write(haps[2*i,j]+' ')
                    output.write(haps[2*i +1,j]+' ')
                output.write(haps[haps.shape[0]-2,haps.shape[1]-1]+' ')
                output.write(haps[haps.shape[0]-1,haps.shape[1]-1]+'\n')
    def __iter__(self,breakListAddress=None):
        self.counter = 0
        if breakListAddress is not None:
            self.set_break_points(breakListAddress)
        return self

    def __next__(self):
        if self.counter == self.it_count:
            raise StopIteration
        new_haps = FPTester.make_haps(self.haps,self.breakList)
        newAddr = os.path.join(self.directory,str(self.counter)+'.haps')
        FPTester.save_haps(new_haps,newAddr)
        self.parameters[PED_ADDRESS] = newAddr
        self.parameters[OUTPUT_ADDRESS] = newAddr[:-5]+'match'
        self.fileName = newAddr[:-5]+'.config'
        self.counter += 1
        return self
    
class GridSearch(TesterBase):

    def __init__(self,directory,pedAddr,mapAddr,bCount,rCount):
        super().__init__(directory)
        self.bStart = bCount[0]
        self.bEnd = bCount[1]
        self.rStart = rCount[0]
        self.rEnd = rCount[1]
        self.parameters[PED_ADDRESS] = pedAddr
        self.parameters[MAP_ADDRESS] = mapAddr


    def __iter__(self):
        self.bHead = self.bStart
        self.rHead = self.rStart
        return self
    
    def __next__(self):
        if self.rHead >= self.rEnd:
            self.rHead = self.rStart
            self.bHead += 1
        if self.bHead >= self.bEnd:
            raise StopIteration
        self.parameters[PERM_COUNT] = self.bHead*self.rHead
        self.parameters[BUCKET_COUNT] = self.bHead
        self.parameters[OUTPUT_ADDRESS] = os.path.join(self.directory,str(self.bHead)+'_'+str(self.rHead)+'.match')
        self.fileName = os.path.join(self.directory,str(self.bHead)+'_'+str(self.rHead)+'.config')
        self.rHead += 1
        return self


class LengthTester(TesterBase):
    def __init__(self, directory,pedAddr,mapAddr,sizeList):
        super().__init__(directory)
        self.parameters[PED_ADDRESS] = pedAddr
        self.parameters[MAP_ADDRESS] = mapAddr
        self.sizeList = sizeList
    
    def __iter__(self):
        self.listHead = 0
        return self
    
    def __next__(self):
        if self.listHead >= len(self.sizeList):
            raise StopIteration
        self.parameters[MIN_LENGTH] =self.sizeList[self.listHead]
        self.parameters[SLICE_LENGTH] =self.sizeList[self.listHead]
        self.parameters[OUTPUT_ADDRESS] = os.path.join(self.directory,str(self.sizeList[self.listHead])+'.match')
        self.fileName = os.path.join(self.directory,str(self.sizeList[self.listHead])+'.config')
        self.listHead += 1 
        return self
        
class ThinnerTester(TesterBase):
    def __init__(self, directory,hapAddr,mapAddr,sampleCount,ratio=2,count=10):
        super().__init__(directory)
        
        self.ratio = ratio
        self.count= count

        self.mapData = np.loadtxt(mapAddr, skiprows=0,
                          dtype={'names': ['chrom', 'RSID', 'gen_dist', 'position'],
                                 'formats': ['i4', 'S10', 'f4', 'i4']})
        self.haps = ThinnerTester.load_ped(hapAddr,sampleCount,self.mapData.shape[0])
    def __iter__(self):
        self.counter = 0
        return self
    
    def __next__(self):
        if self.counter >= self.count:
            raise StopIteration
        self.make_map_ped()
        self.parameters[OUTPUT_ADDRESS] = os.path.join(self.directory,'thinned'+str(self.counter)+'_'+str(self.ratio)+'.match')
        self.fileName = os.path.join(self.directory,str(self.counter)+'.config')
        self.counter += 1 
        return self

    @staticmethod
    def load_ped(pedAddr,indCount,dim):
        haps = np.zeros((indCount*2,dim),dtype=np.dtype('U1'))
        counter = 0 
        with open(pedAddr) as pedFile:
            for line in pedFile:
                data = line.strip().split()
                haps[2*counter,:] = data[6::2]
                haps[2*counter+1,:] = data[7::2]
                counter += 1
        return haps

    @staticmethod
    def save_map(mapAddr,mapArray):
        with open(mapAddr,'w') as mapFile:
            for mapItem in mapArray:
                mapFile.write('\t'.join([str(item) for item in mapItem])+'\n')

        
    def make_map_ped(self):
        snp2Remove = np.random.choice(self.ratio,self.mapData.shape[0]//self.ratio)
        for i in range(snp2Remove.shape[0]):
            snp2Remove[i] = 2*i+snp2Remove[i]
        mask = np.zeros((self.mapData.shape[0]),dtype=np.dtype('bool'))
        mask[:] = True
        mask[snp2Remove] = False
        newMapAddr = os.path.join(self.directory,'thinned_'+str(self.counter)+'.map')
        newPedAddr = os.path.join(self.directory,'thinned_'+str(self.counter)+'.ped')
        ThinnerTester.save_map(newMapAddr,self.mapData[mask])
        #np.savetxt(newMapAddr,self.mapData[mask],delimiter='\t',fmt=['d','s','f','d'])
        FPTester.save_haps(self.haps[:,mask],newPedAddr)
        self.parameters[MAP_ADDRESS] = newMapAddr
        self.parameters[PED_ADDRESS] = newPedAddr
        
