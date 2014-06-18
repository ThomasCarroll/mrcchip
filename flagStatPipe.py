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

module_add("samtools/0.1.18")

fastq = sys.argv[1]
baseName = sys.argv[2]
genome = sys.argv[3]
outputPath = sys.argv[4]

bamDir = os.path.join(outputPath,"AlignedData")
bamOut = os.path.join(bamDir,baseName+".bam")


print os.environ["LOADEDMODULES"]

flagstatPath = os.path.join(outputPath,"flagstat")

if not os.path.exists(flagstatPath):
  os.makedirs(flagstatPath)

flagStatOut = os.path.join(flagstatPath,baseName+".flagStat")

if not os.path.isfile(flagStatOut):
  p = subprocess.Popen(["/bin/bash",'-i',"-c","samtools flagstat "+" "+bamOut+" > "+flagStatOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()

