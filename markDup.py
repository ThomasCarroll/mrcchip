#!/usr/bin/python -O

import subprocess                                                 
import os                                                         
import sys                                                        


def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout


fastq = sys.argv[1]
baseName = sys.argv[2]
genome = sys.argv[3]
outputPath = sys.argv[4]
#strandSpecificity = sys.argv[5]
#fastq = "/csc/rawdata/Cscbioinf/test.fq"
#outputPath = "/csc/analysis/Cscbioinf/Temp/Test2"
#baseName = "FiftyG_R1"
#genome = "dm3"
#strandSpecificity = "none"


bamDir = os.path.join(outputPath,"AlignedData")
bamToCount = os.path.join(bamDir,baseName+".bam")
outputBam = os.path.join(bamDir,baseName+"DupMarked.bam")
outputMetrics = os.path.join(bamDir,baseName+".metrics")

markDupCmd = "java -Xmx4g -jar /apps/picard/1.90/picard-tools-1.90/MarkDuplicates.jar  CREATE_INDEX=true ASSUME_SORTED=true Input="+bamToCount+" Output="+outputBam+" METRICS_FILE="+outputMetrics+" VALIDATION_STRINGENCY=SILENT"
print markDupCmd

if not os.path.isfile(outputBam):
  p = subprocess.Popen(["/bin/bash",'-i',"-c",markDupCmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
