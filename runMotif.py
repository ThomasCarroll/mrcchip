#!/usr/bin/python -O

import subprocess                                                 
import os                                                         
import sys                                                        


def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout

module_add("python/2.7.3")
module_add("meme/4.9.0")

print "hello"

genomeFastaFiles = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9.fa","hg19":"/csc/rawdata/Cscbioinf/bioinfResources/Homo_sapiens/Ensembl/GRCh37/Sequence/BWAIndex/genome.fa"}

fastq = sys.argv[1]
baseNameSample = sys.argv[2]
genome = sys.argv[3]
baseNameInput = sys.argv[4]
outputPath = sys.argv[5]

bamDir = os.path.join(outputPath,"AlignedData")
macsDir = os.path.join(outputPath,"Macs")
outputDir = os.path.join(outputPath,"Motif",baseNameSample)
if not os.path.exists(outputDir):
  os.makedirs(outputDir)
outputPathForSequence = os.path.join(outputPath,"Motif",baseNameSample,baseNameSample+".fa")
outputPathForMeme = os.path.join(outputPath,"Motif",baseNameSample,baseNameSample+"_MotifDir")
print outputPathForSequence
print outputPathForMeme

bamSample = os.path.join(bamDir,baseNameSample+".bam")
bamInput = os.path.join(bamDir,baseNameInput+".bam")
PeaksName = os.path.join(macsDir,baseNameSample+"_WithInput_"+baseNameInput+"_peaks.bed")

extractCMD = "python /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/extractSequenceUnderPeak.py "+PeaksName+" "+genomeFastaFiles[genome]+" "+outputPathForSequence+" 200"
#if not os.path.isfile(outPutName+"_peaks.bed"):
p = subprocess.Popen(["/bin/bash",'-i',"-c",extractCMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout,stderr = p.communicate()
print extractCMD
memeCMD = "meme-chip "+outputPathForSequence+" -db /csc/rawdata/Cscbioinf/bioinfResources/Jaspar/sites/Motifs.meme -oc "+outputPathForMeme
p = subprocess.Popen(["/bin/bash",'-i',"-c",memeCMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout,stderr = p.communicate()
print stderr
print stdout
print memeCMD
