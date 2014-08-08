#!/usr/bin/python -O
#PBS -N myjob
#PBS -l select=1:ncpus=9:mem=12GB
#PBS -l walltime=70:00:00
from time import sleep

sleep(30)

import subprocess                                                 
import os                                                         
import sys                                                        

def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout

module_add("bio-bwa/0.7.5a")

genomeFastaFiles = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9.fa","hg19":"/csc/rawdata/Cscbioinf/bioinfResources/Homo_sapiens/Ensembl/GRCh37/Sequence/BWAIndex/genome.fa"}

#genome = "mm9"
#fastq = "/csc/rawdata/Merkenshlager/131209_SN172_0451_BD26VHACXX_Merkenschlager/Unaligned/Sample_3InpVS/3InpVS_ACAGTG_L003_R1_001.fastq.gz"
#baseName = "/csc/rawdata/Dillon/DillonTest/test"
fastq = sys.argv[1]
baseName = sys.argv[2]
genome = sys.argv[3]
outputPath = sys.argv[4]

outputPath = os.path.join(outputPath,"AlignedData")
if not os.path.exists(outputPath):
  os.makedirs(outputPath)

saiOut = os.path.join(outputPath,baseName+".sai")
samOut = os.path.join(outputPath,baseName+".sam")
bamOut = os.path.join(outputPath,baseName+".bam")
dupMarkedBam = os.path.join(outputPath,baseName+"DupMarked.bam")
trimmedFQOut = os.path.join(outputPath,baseName+"trimmed.fq.gz")
if os.path.exists(bamOut):
  if os.stat(bamOut).st_size == 0:
    os.remove(bamOut)
    if os.path.exists(dupMarkedBam):
      os.remove(dupMarkedBam)      

print os.environ["LOADEDMODULES"]

if not os.path.isfile(genomeFastaFiles[genome]) or not os.path.isfile(genomeFastaFiles[genome]+".bwt") or not os.path.isfile(genomeFastaFiles[genome]+".sa"):
  if os.path.isfile(genomeFastaFiles[genome]): 
    print "Not all necessary index files found..indexing"
    #p = subprocess.Popen(["/bin/bash",'-i',"-c","bwa index -a bwtsw "+genome], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout,stderr = p.communicate()
  else:
    "Fasta file is not found"
elif os.path.isfile(genomeFastaFiles[genome]) and os.path.isfile(genomeFastaFiles[genome]+".bwt") and os.path.isfile(genomeFastaFiles[genome]+".sa"):
  if not os.path.isfile(bamOut):
    trimCMD1 = "zcat "+fastq+" | python  /csc/rawdata/Cscbioinf/bioinfResources/trimFQ.py 36 | gzip - > "+trimmedFQOut
    print trimCMD1
    p = subprocess.Popen(["/bin/bash",'-i',"-c",trimCMD1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()    
    p = subprocess.Popen(["/bin/bash",'-i',"-c","bwa aln -t 8 "+genomeFastaFiles[genome]+" "+trimmedFQOut+" >"+saiOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    if p.returncode == 0:
      p = subprocess.Popen(["/bin/bash",'-i',"-c","bwa samse "+genomeFastaFiles[genome]+" "+saiOut+" "+trimmedFQOut+" >"+samOut], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout,stderr = p.communicate()
    else:
      print stderr, "\nAlignment-Failed\n"
    if p.returncode == 0:
      p = subprocess.Popen(["/bin/bash",'-i',"-c","java -jar /apps/picard/1.90/picard-tools-1.90/SortSam.jar Input="+samOut+" Output="+bamOut+" SORT_ORDER=coordinate VALIDATION_STRINGENCY=SILENT CREATE_INDEX=true"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      stdout,stderr = p.communicate()
    else:
      print stderr, "\nResorting Failed\n"

if os.path.exists(saiOut):
  os.remove(saiOut)
if os.path.exists(samOut):
  os.remove(samOut)
