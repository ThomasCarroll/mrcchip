#!/usr/bin/python -O
#PBS -N myjob
#PBS -l select=1:ncpus=9:mem=12GB
#PBS -l walltime=70:00:00

import subprocess                                                 
import os                                                         
import sys                                                        

def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout

module_add("bedtools/2.17.0")

genomeChrLengths = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9.chrLengths"}

fastq = sys.argv[1]
baseName = sys.argv[2]
genome = sys.argv[3]
outputPath = sys.argv[4]
bamDir = os.path.join(outputPath,"AlignedData")
bigWigDir = os.path.join(outputPath,"CoveragePileup")
if not os.path.exists(bigWigDir):
  os.makedirs(bigWigDir)


bigWigExec = "/csc/rawdata/Cscbioinf/bioinfResources/pipelineTools/bedGraphToBigWig"
saiOut = os.path.join(bamDir,baseName+".sai")
samOut = os.path.join(bamDir,baseName+".sam")
bamOut = os.path.join(bamDir,baseName+".bam")

bedGraphOut = os.path.join(bigWigDir,baseName+".bedGraph")
bigWigOut = os.path.join(bigWigDir,baseName+".bw")

if not os.path.isfile(bigWigOut):
  p = subprocess.Popen(["/bin/bash",'-i',"-c","genomeCoverageBed -bga -ibam "+bamOut+" > "+bedGraphOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
  if p.returncode == 0:
  	p = subprocess.Popen(["/bin/bash",'-i',"-c",""+bigWigExec+" "+bedGraphOut+" "+genomeChrLengths[genome]+" "+bigWigOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout,stderr = p.communicate()
  else:
    print stderr, "\nMaking bedGraph Failed\n"

if os.path.exists(bedGraphOut):
  os.remove(bedGraphOut)
