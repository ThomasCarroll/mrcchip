import csv
import sys
import os
import subprocess

#csvFile = "/csc/rawdata/Cscbioinf/bioinfResources/ziweiChipTestNucleosome2.csv"
csvFile = "/csc/analysis/Cscbioinf/ZLiangNucleosome/ziweiChipTestNucleosome2.csv"
baseDir = "/csc/analysis/Cscbioinf/ZLiangNucleosome/"
#csvFile = sys.argv[1]
#baseDir = sys.argv[2] 
mergedGenome = "mm9"


j = 0
stdoutAlignDict = {}
stdoutAlignDict2 = {}
stdoutAlignSampe = {}
SampleList = []
SampleName = []

with open(csvFile, 'rb') as csvfile:
 spamreader = csv.reader(csvfile,delimiter='\t',quotechar='|')
 for row in spamreader:
  read1,read2 = row[0].split(",")
  SampleName.append(row[1])  
  jobName = os.path.basename(row[1])
  SampleList.append(jobName)
  submitCmdRead1 = "echo /csc/rawdata/Cscbioinf/bioinfResources/pairedAlign.py"+" "+read1+" "+row[1]+"read1"+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=4:mem=12GB -l walltime=70:00:00 -N "+jobName[7:14]+"Align"
  print submitCmdRead1
  pRead1 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdRead1],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdoutRead1,stderrRead1 = pRead1.communicate()
  stdoutAlignDict[jobName] = stdoutRead1
  submitCmdRead2 = "echo /csc/rawdata/Cscbioinf/bioinfResources/pairedAlign.py"+" "+read2+" "+row[1]+"read2"+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=4:mem=12GB -l walltime=70:00:00 -N "+jobName[7:14]+"Align"
  print submitCmdRead2
  pRead2 = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdRead2],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdoutRead2,stderrRead2 = pRead2.communicate()
  stdoutAlignDict2[jobName] = stdoutRead2
  submitCmdRead3 = "echo /csc/rawdata/Cscbioinf/bioinfResources/sampe.py"+" "+row[0]+" "+row[1]+" "+row[2]+" "+baseDir+" | qsub -l select=1:ncpus=4:mem=30GB -l walltime=70:00:00 -N "+jobName[7:14]+"Align"+" -W depend=afterok:"+stdoutRead2.strip()+":"+stdoutRead1.strip()
  print submitCmdRead3
  pSampe = subprocess.Popen(["/bin/bash",'-i',"-c",submitCmdRead3],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  stdoutSampe,stderSampe = pSampe.communicate()
  stdoutAlignSampe[jobName] = stdoutRead2



