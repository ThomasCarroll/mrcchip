#!/usr/bin/python -O

import subprocess                                                 
import os                                                         
import sys                                                        

def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout

module_add("samtools/0.1.18")

inputBams = sys.argv[1]
outputBam = sys.argv[2]
baseDir = sys.argv[3]
print inputBams
outputPath = os.path.join(baseDir,"AlignedData","")
outputBam = os.path.join(baseDir,"AlignedData",outputBam)

print os.environ["LOADEDMODULES"]

if not os.path.isfile(outputBam):
  inputForPicard = inputBams.split(";")
  inputStringForPicard = " ".join(["INPUT="+outputPath+s+".bam" for s in inputForPicard])
  mergeCmd = "java -jar /apps/picard/1.90/picard-tools-1.90/MergeSamFiles.jar "+inputStringForPicard+" OUTPUT="+outputBam+" CREATE_INDEX=true VALIDATION_STRINGENCY=SILENT"
  print mergeCmd
  p = subprocess.Popen(["/bin/bash",'-i',"-c",mergeCmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
