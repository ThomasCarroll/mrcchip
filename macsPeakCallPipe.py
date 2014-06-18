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

module_add("macs/1.4.1")

genomeLengths = {"mm9":"mm"}

fastq = sys.argv[1]
baseNameSample = sys.argv[2]
genome = sys.argv[3]
baseNameInput = sys.argv[4]
outputPath = sys.argv[5]

bamDir = os.path.join(outputPath,"AlignedData")
macsDir = os.path.join(outputPath,"AlignedData")
if not os.path.exists(macsDir):
  os.makedirs(macsDir)


bamSample = os.path.join(bamDir,baseNameSample+".bam")
bamInput = os.path.join(bamDir,baseNameInput+".bam")
outPutName = os.path.join(macsDir,baseNameSample+"_WithInput_"+baseNameInput)

macsCmd = "macs14 -t "+bamSample+" -c "+bamInput+" -g "+genomeLengths[genome]+" -n "+outPutName
if not os.path.isfile(outPutName+"_peaks.bed"):
  p = subprocess.Popen(["/bin/bash",'-i',"-c",macsCmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
