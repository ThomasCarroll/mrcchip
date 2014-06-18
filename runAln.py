import csv
import sys
import os
import subprocess
from collections import Counter

#csvFile = "/csc/analysis/Cscbioinf/Ikaros/IkarosChIPforPipe.csv"
#baseDir = "/csc/analysis/Cscbioinf/Ikaros/"
csvFile = "/csc/analysis/Cscbioinf/IkarosRelated/RelatedToIkarosChIPforPipe2.csv"
baseDir = "/csc/analysis/Cscbioinf/IkarosRelated/"
#csvFile = sys.argv[1]
#baseDir = sys.argv[2] 
#mergedGenome = sys.argv[2] 
mergedGenome = "mm9"

errorPath = os.path.join(baseDir,"errors","")
outputPath = os.path.join(baseDir,"outputs","")

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
  if row[0] != "Merged":
    if row[4] != "NA":
      toMergeList.append(row[4])
    SampleName.append(row[1])  
    jobName = os.path.basename(row[1])
    SampleList.append(jobName)
    submitCmd = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/alnAndSortPipe.py"+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -h -l select=1:ncpus=4:mem=12GB -l walltime=70:00:00 -N "+jobName[7:14]+"Align"+" -e "+errorPath+" -o "+outputPath
    print submitCmd
    p = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    stdoutAlignDict[jobName] = stdout
    submitCmd3 = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/bedGraphAndBigWigPipe.py"+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+jobName[0:7]+"bigwig"+" -W depend=afterok:"+stdout.strip()+" -e "+errorPath+" -o "+outputPath
    print submitCmd3
    p3 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout3,stderr3 = p3.communicate()
    stdoutBigWigDict[jobName] = stdout3
    submitCmd2 = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/flagStatPipe.py"+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+jobName[0:7]+"flagStat"+" -W depend=afterok:"+stdout.strip()+" -e "+errorPath+" -o "+outputPath
    p2 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd2],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout2,stderr2 = p2.communicate() 
    stdoutflagStatDict[jobName] = stdout2
    print submitCmd2
    submitCmdMarkDups = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/markDup.py"+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+jobName[0:7]+"ChIPQC"+" -W depend=afterok:"+stdout.strip()+" -e "+errorPath+" -o "+outputPath
    pMarkDups = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdMarkDups],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutMarkDups,stderrMarkDups = pMarkDups.communicate() 
    stdoutMarkDupsDict[jobName] = stdoutMarkDups
    print submitCmdMarkDups  
    submitCmdChIPQC = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/runChIPQC.py"+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+jobName[0:7]+"ChIPQC"+" -W depend=afterok:"+stdoutMarkDups.strip()+" -e "+errorPath+" -o "+outputPath
    pChIPQC = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdChIPQC],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutChIPQC,stderrChIPQC = pChIPQC.communicate() 
    stdoutChIPQCDict[jobName] = stdoutChIPQC
    print submitCmdChIPQC  



mergeDict = dict(Counter(toMergeList)) 
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
    picardMergeCMD = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/mergePipe.py "+inputToMerge+" "+outputBam+" "+baseDir+" "+" | qsub -h -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+os.path.basename(outputBam)[0:7]+"merge"+mergingDependencies+" -e "+errorPath+" -o "+outputPath     
    pMerge = subprocess.Popen(["/bin/bash",'-i',"-c",picardMergeCMD],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutMerge,stderrMerge = pMerge.communicate() 
    stdoutMergeDict[os.path.basename(mergedBamName[mergeIndex])] = stdoutMerge
    print picardMergeCMD
    submitCmdMarkDupsMerge = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/markDup.py"+" "+"Dummy"+" "+mergedBamName[mergeIndex]+" "+"Genome"+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+jobName[0:7]+"ChIPQC"+" -W depend=afterok:"+stdoutMerge.strip()+" -e "+errorPath+" -o "+outputPath
    pMarkDupsMerge = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdMarkDupsMerge],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutMarkDupsMerge,stderrMarkDupsMerge = pMarkDupsMerge.communicate() 
    stdoutMarkDupsDictMerge[jobName] = stdoutMarkDupsMerge
    print submitCmdMarkDupsMerge  
    submitCmdChIPQCMerge = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/runChIPQC.py"+" "+mergedBamName[mergeIndex]+" "+mergedGenome+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+jobName[0:7]+"ChIPQC"+" -W depend=afterok:"+stdoutMarkDupsMerge.strip()+" -e "+errorPath+" -o "+outputPath
    pChIPQCMerge = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdChIPQCMerge],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutChIPQCMerge,stderrChIPQCMerge = pChIPQCMerge.communicate() 
    stdoutChIPQCDictMerge[jobName] = stdoutChIPQCMerge
    print submitCmdChIPQCMerge  
    mergeIndex += 1


allSampleDictionay = stdoutAlignDict.copy()
allSampleDictionay.update(stdoutMergeDict)


with open(csvFile, 'rb') as csvfile:
 spamreader = csv.reader(csvfile,delimiter='\t',quotechar='|')
 for row in spamreader:
  print row[3]
  print SampleList
  if row[3] in SampleList:
   jobName = os.path.basename(row[1])
   submitCmd4 = "echo /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/macsPeakCallPipe.py"+" "+row[0]+" "+row[1]+" "+row[2]+" "+row[3]+" "+baseDir+" | qsub -l select=1:ncpus=1:mem=12GB -l walltime=70:00:00 -N "+jobName[0:7]+"macs"+" -W depend=afterok:"+allSampleDictionay[jobName].strip()+":"+allSampleDictionay[row[3]].strip()+" -e "+errorPath+" -o "+outputPath
   p4 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmd4],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
   stdout4,stderr4 = p4.communicate() 
   stdoutMacsPeakCallDict[jobName] = stdout4
   print submitCmd4
   

for sampleJob in allSampleDictionay:
  pFinal = subprocess.Popen(["/bin/bash",'-i',"-c","qrls " + allSampleDictionay[sampleJob].strip()],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdout4,stderr4 = pFinal.communicate() 
