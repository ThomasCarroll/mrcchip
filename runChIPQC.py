#!/usr/bin/python -O

import subprocess                                                 
import os                                                         
import sys
import re                                                        


def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout


baseName = sys.argv[1]
genome = sys.argv[2]
outputPath = sys.argv[3]


blacklist = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9-blacklist.bed"}


module_add("R/3.1.0")

bamDir = os.path.join(outputPath,"AlignedData")
chipqcDir = os.path.join(outputPath,"chipqc")
if not os.path.exists(chipqcDir):
  os.makedirs(chipqcDir)

bamFile = os.path.join(bamDir,baseName+"DupMarked.bam")
chipqcResult = os.path.join(chipqcDir,baseName+"DupMarked.RData")
chipqccmd = "Rscript /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/runChIPQC.r "+bamFile+" "+genome+" "+blacklist[genome]
print chipqccmd
if not os.path.isfile(chipqcResult):
  p = subprocess.Popen(["/bin/bash",'-i',"-c",chipqccmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
