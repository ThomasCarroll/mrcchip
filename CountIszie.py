import pysam
import sys
import Pyrex
import os
import math

BamFile = sys.argv[1]
samFile = pysam.Samfile(BamFile,"rb")
AllMapped = samFile.mapped
headerOriginal = samFile.header
Range1C = 0
Range2C = 0
Range3C = 0
Range4C = 0
Range5C = 0
count = 0
outfileRange1 = pysam.Samfile(str(BamFile)+"Range1.bam","wb",header=headerOriginal)
outfileRange2 = pysam.Samfile(str(BamFile)+"Range2.bam","wb",header=headerOriginal)
outfileRange3 = pysam.Samfile(str(BamFile)+"Range3.bam","wb",header=headerOriginal)
outfileRange4 = pysam.Samfile(str(BamFile)+"Range4.bam","wb",header=headerOriginal)
outfileRange5 = pysam.Samfile(str(BamFile)+"Range5.bam","wb",header=headerOriginal)
for alignedread in samFile.fetch():
	if math.fabs(alignedread.isize) < 30:
		outfileRange1.write(alignedread)
		Range1C += 1
	if (math.fabs(alignedread.isize) >= 30) & (math.fabs(alignedread.isize) < 80):
		outfileRange2.write(alignedread)
		Range2C += 1
	if (math.fabs(alignedread.isize) >= 80) & (math.fabs(alignedread.isize) < 110):
		outfileRange3.write(alignedread)
		Range3C += 1
	if (math.fabs(alignedread.isize) >= 110) & (math.fabs(alignedread.isize) < 140):
		outfileRange4.write(alignedread)
		Range4C += 1
	if (math.fabs(alignedread.isize) >= 140):
		outfileRange5.write(alignedread)
		Range5C += 1
	count += 1		

outfileRange1.close()
outfileRange2.close()
outfileRange3.close()
outfileRange4.close()
outfileRange5.close()
pysam.index(str(BamFile)+"Range1.bam")
pysam.index(str(BamFile)+"Range2.bam")
pysam.index(str(BamFile)+"Range3.bam")
pysam.index(str(BamFile)+"Range4.bam")
pysam.index(str(BamFile)+"Range5.bam")
samFile.close()
fileLog = open(str(BamFile)+"_fileLog.log","wb")
fileLog.write(str(Range1C)+"\n"+str(Range2C)+"\n"+str(Range3C)+str(Range4C)+"\n"+str(Range5C)+"\n")
fileLog.close()
