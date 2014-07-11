#!/apps/python/2.7.3/bin/python -O
import csv
import sys
import os
import subprocess
from collections import Counter
import argparse
import textwrap


parser = argparse.ArgumentParser(prog='./runAln.py',usage='%(prog)s -S(--samplesheet) [path_to_samplesheet] -D(--directory) [path_to_directory] -G(--genome) [genome]',
  formatter_class=argparse.RawDescriptionHelpFormatter,description=textwrap.dedent('''\
         Welcome to the ChIP-seq pipeline
         --------------------------------
        This tools was written for the MRC CSC bioinformatics team.
        It includes an automated procedure for the alignment, 
        processing , QC and analysis of ChIP-seq and other enrichment
        sequencing data.
        
        For a full description please see our github page and website
        Github site: https://github.com/ThomasCarroll/mrcchip 
        Manual site: http://thomascarroll.github.io/mrcchip/

        For any other problems please contact Tom Carroll (thomas.carroll@imperial.ac.uk)
         ''')
  )
parser.add_argument("-S","--samplesheet",help="The full path to samplesheet containing sample and metadata information",required=True)
parser.add_argument("-D","--directory", help="The full path to directory where output directories will be created",required=True)
parser.add_argument("-G","--genome", help="The genome to be used",required=True,choices=['hg19', 'mm9', 'dm3'])
args = parser.parse_args()

baseForPipeline = os.path.dirname(sys.argv[0])
print baseForPipeline
baseForPipeline = "/csc/rawdata/Cscbioinf/bioinfResources/chippipeline/"
#csvFile = "/csc/analysis/Cscbioinf/Ikaros/IkarosChIPforPipe.csv"
#baseDir = "/csc/analysis/Cscbioinf/Ikaros/"
csvFile = "/csc/analysis/Cscbioinf/2014020_sSauer_Extra/chipsSauer4.csv"
baseDir = "/csc/analysis/Cscbioinf/2014020_sSauer_Extra/"
mergedGenome = "mm9"

csvFile = args.samplesheet
baseDir = args.directory 
mergedGenome = args.genome 

errorPath = os.path.join(baseDir,"errors","")
outputPath = os.path.join(baseDir,"outputs","")
submitPath = os.path.join(baseDir,"submissions.txt")
if not os.path.exists(errorPath):
  os.makedirs(errorPath)

if not os.path.exists(outputPath):
  os.makedirs(outputPath)

f = open(submitPath, 'w')

j = 0
stdoutAlignDict = {}
stdoutBigWigDict = {}
stdoutflagStatDict = {}
stdoutMacsPeakCallDict = {}
stdoutMergeDict = {}
stdoutChIPQCDict = {} 
stdoutChIPQCDictMerge = {} 
stdoutMarkDupsDict = {}
stdoutMarkDupsDictMerge = {}
SampleList = []
SampleName = []
toMergeList = []
bamsToMerge = []

with open(csvFile, 'rb') as csvfile:
 spamreader = csv.reader(csvfile,delimiter='\t',quotechar='|')
 for row in spamreader:
  jobName = os.path.basename(row[1])
  SampleList.append(jobName)
  SampleName.append(row[1])
  toMergeList.append(row[4])  
  if row[0] != "Merged":  
    submitCmd = "echo "+os.path.join(baseForPipeline,"alnAndSortPipe.py")+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -h -l select=1:ncpus=4:mem=12GB -l walltime=70:00:00  -e "+errorPath+" -o "+outputPath
    print submitCmd
    p = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    f.write(stdout.strip()+"\t"+submitCmd+"\n")
    stdoutAlignDict[jobName] = stdout
    submitCmd3 = "echo "+os.path.join(baseForPipeline,"bedGraphAndBigWigPipe.py")+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00  -W depend=afterok:"+stdout.strip()+" -e "+errorPath+" -o "+outputPath
    print submitCmd3
    p3 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout3,stderr3 = p3.communicate()
    f.write(stdout3.strip()+"\t"+submitCmd3+"\n")    
    stdoutBigWigDict[jobName] = stdout3
    submitCmd2 = "echo "+os.path.join(baseForPipeline,"flagStatPipe.py")+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -W depend=afterok:"+stdout.strip()+" -e "+errorPath+" -o "+outputPath
    p2 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd2],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout2,stderr2 = p2.communicate()
    f.write(stdout2.strip()+"\t"+submitCmd2+"\n")     
    stdoutflagStatDict[jobName] = stdout2
    print submitCmd2
    submitCmdMarkDups = "echo "+os.path.join(baseForPipeline,"markDup.py")+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -W depend=afterok:"+stdout.strip()+" -e "+errorPath+" -o "+outputPath
    pMarkDups = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdMarkDups],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutMarkDups,stderrMarkDups = pMarkDups.communicate() 
    stdoutMarkDupsDict[jobName] = stdoutMarkDups
    print submitCmdMarkDups
    f.write(stdoutMarkDups.strip()+"\t"+submitCmdMarkDups+"\n")        
    submitCmdChIPQC = "echo "+os.path.join(baseForPipeline,"runChIPQC.py")+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -W depend=afterok:"+stdoutMarkDups.strip()+" -e "+errorPath+" -o "+outputPath
    pChIPQC = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdChIPQC],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutChIPQC,stderrChIPQC = pChIPQC.communicate() 
    f.write(stdoutChIPQC.strip()+"\t"+submitCmdChIPQC+"\n")    
    stdoutChIPQCDict[jobName] = stdoutChIPQC
    print submitCmdChIPQC  



mergeDict = dict(Counter(toMergeList)) 
del mergeDict["NA"]
mergedBamName = []
for toMerge in mergeDict:
  sampleNameIndex = 0
  tempbamsToMerge = []
  for mergeName in toMergeList:
    if mergeName == toMerge:
      tempbamsToMerge.append(SampleName[sampleNameIndex])
    sampleNameIndex += 1
  if len(tempbamsToMerge) > 0:
    bamsToMerge.append(tempbamsToMerge) 
    mergedBamName.append(toMerge)     


if len(mergedBamName) > 0:
  mergeIndex = 0
  for mergedBams in bamsToMerge:
    mergingDependencies = " -W depend=afterok"
    inputToMerge = ""
    for bam in mergedBams:
      mergingDependencies = mergingDependencies+":"+stdoutAlignDict[bam].strip()
    inputToMerge = "\\\\\;".join(mergedBams)
    outputBam = ""+mergedBamName[mergeIndex]+".bam"
    picardMergeCMD = "echo "+os.path.join(baseForPipeline,"mergePipe.py")+" "+inputToMerge+" "+outputBam+" "+baseDir+" "+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 "+mergingDependencies+" -e "+errorPath+" -o "+outputPath     
    pMerge = subprocess.Popen(["/bin/bash",'-i',"-c",picardMergeCMD],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutMerge,stderrMerge = pMerge.communicate() 
    stdoutMergeDict[os.path.basename(mergedBamName[mergeIndex])] = stdoutMerge
    print picardMergeCMD
    f.write(stdoutMerge.strip()+"\t"+picardMergeCMD+"\n")     
    submitCmdMarkDupsMerge = "echo "+os.path.join(baseForPipeline,"markDup.py")+" "+"Dummy"+" "+mergedBamName[mergeIndex]+" "+"Genome"+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -W depend=afterok:"+stdoutMerge.strip()+" -e "+errorPath+" -o "+outputPath
    pMarkDupsMerge = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdMarkDupsMerge],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutMarkDupsMerge,stderrMarkDupsMerge = pMarkDupsMerge.communicate() 
    stdoutMarkDupsDictMerge[jobName] = stdoutMarkDupsMerge
    print submitCmdMarkDupsMerge
    f.write(stdoutMarkDupsMerge.strip()+"\t"+submitCmdMarkDupsMerge+"\n") 
    submitCmdChIPQCMerge = "echo "+os.path.join(baseForPipeline,"runChIPQC.py")+" "+mergedBamName[mergeIndex]+" "+mergedGenome+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -W depend=afterok:"+stdoutMarkDupsMerge.strip()+" -e "+errorPath+" -o "+outputPath
    pChIPQCMerge = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdChIPQCMerge],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutChIPQCMerge,stderrChIPQCMerge = pChIPQCMerge.communicate() 
    stdoutChIPQCDictMerge[jobName] = stdoutChIPQCMerge
    print submitCmdChIPQCMerge
    f.write(stdoutChIPQCMerge.strip()+"\t"+submitCmdChIPQCMerge+"\n")       
    mergeIndex += 1


allSampleDictionay = stdoutAlignDict.copy()
allSampleDictionay.update(stdoutMergeDict)
SampleList.extend(mergedBamName)

with open(csvFile, 'rb') as csvfile:
 spamreader = csv.reader(csvfile,delimiter='\t',quotechar='|')
 for row in spamreader:
  #print row[3]
  #print SampleList
  if row[3] in SampleList:
   jobName = os.path.basename(row[1])
   submitCmd4 = "echo "+os.path.join(baseForPipeline,"macsPeakCallPipe.py")+" "+row[0]+" "+row[1]+" "+row[2]+" "+row[3]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -W depend=afterok:"+allSampleDictionay[jobName].strip()+":"+allSampleDictionay[row[3]].strip()+" -e "+errorPath+" -o "+outputPath
   p4 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd4],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   stdout4,stderr4 = p4.communicate() 
   stdoutMacsPeakCallDict[jobName] = stdout4
   print submitCmd4
   f.write(stdout4.strip()+"\t"+submitCmd4+"\n")     
 



allJobs = stdoutChIPQCDict.values()+stdoutChIPQCDictMerge.values()+stdoutMacsPeakCallDict.values()

alignJobrequirment = "-W depend=afterany"
for alignJob in allJobs:
    alignJobrequirment = alignJobrequirment+":"+alignJob.strip()


PoolResultsCMD = "echo "+os.path.join(baseForPipeline,"poolResults.py")+" "+csvFile+" "+mergedGenome+" "+baseDir+" | qsub -l select=1:ncpus=4:mem=20GB -l walltime=70:00:00 "+alignJobrequirment+" -e "+errorPath+" -o "+outputPath
pFinal = subprocess.Popen(["/bin/bash",'-i',"-c",PoolResultsCMD],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
print PoolResultsCMD
stdFinalOut,stdFinalError = pFinal.communicate()
f.write(stdFinalOut.strip()+"\t"+PoolResultsCMD+"\n")    

for sampleJob in allSampleDictionay:
  pFinal = subprocess.Popen(["/bin/bash",'-i',"-c","qrls " + allSampleDictionay[sampleJob].strip()],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdout4,stderr4 = pFinal.communicate() 

f.close()
