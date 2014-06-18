#!/usr/bin/python -O
#PBS -N myjob
#PBS -l select=1:ncpus=4:mem=12GB
#PBS -l walltime=70:00:00


import subprocess                                                 
import os                                                         
import sys                                                        

def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout

module_add("bio-bwa/0.7.5a")
module_add("bedtools/2.17.0")

bigWigExec = "/csc/rawdata/Cscbioinf/bioinfResources/pipelineTools/bedGraphToBigWig"


genomeFastaFiles = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9.fa"}
genomeChrLengths = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9.chrLengths"}

genome = "mm9"
fastq = "/csc/rawdata/Dillon/Aphi30_GGCTAC_L003_R1_001.fastq"
baseName = "/csc/rawdata/Dillon/DillonTest/test"

saiOut = baseName+".sai"
samOut = baseName+".sam"
bamOut = baseName+".bam"
bedGraphOut = baseName+".bedGraph"
bigWigOut = baseName+".bw"

print os.environ["LOADEDMODULES"]

if not os.path.isfile(genomeFastaFiles["mm9"]) or not os.path.isfile(genomeFastaFiles["mm9"]+".bwt") or not os.path.isfile(genomeFastaFiles["mm9"]+".sa"):
  if os.path.isfile(genomeFastaFiles["mm9"]): 
    print "Not all necessary index files found..indexing"
    #p = subprocess.Popen(["/bin/bash",'-i',"-c","bwa index -a bwtsw "+genome], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout,stderr = p.communicate()
  else
    "Fasta file is not found"
elif os.path.isfile(genomeFastaFiles["mm9"]) and os.path.isfile(genomeFastaFiles["mm9"]+".bwt") and os.path.isfile(genomeFastaFiles["mm9"]+".sa"):
  p = subprocess.Popen(["/bin/bash",'-i',"-c","bwa aln "+genomeFastaFiles["mm9"]+" "+fastq+" >"+saiOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
  if p.returncode == 0:
    p = subprocess.Popen(["/bin/bash",'-i',"-c","bwa samse "+genomeFastaFiles["mm9"]+" "+saiOut+" "+fastq+" >"+samOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
  else:
    print stderr, "\nAlignment-Failed\n"

  if p.returncode == 0:
    p = subprocess.Popen(["/bin/bash",'-i',"-c","java -jar /apps/picard/1.90/picard-tools-1.90/SortSam.jar Input="+samOut+" Output="+bamOut+" SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT CREATE_INDEX=true"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
  else:
    print stderr, "\nResorting Failed\n"
  if p.returncode == 0:
    p = subprocess.Popen(["/bin/bash",'-i',"-c","genomeCoverageBed -bga -ibam "+bamOut+" > "+bedGraphOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
  else:
    print stderr, "\nMaking bedGraph Failed\n"
  if p.returncode == 0:
p = subprocess.Popen(["/bin/bash",'-i',"-c",""+bigWigExec+" "+bedGraphOut+" "+genomeChrLengths["mm9"]+" "+bigWigOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout,stderr = p.communicate()
  else:
    print stderr, "\nMaking bigwig Failed\n"


