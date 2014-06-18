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

module_add("bio-bwa/0.7.5a")

genomeFastaFiles = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9.fa"}
#genome = "mm9"
#fastq = "/csc/rawdata/Merkenshlager/131209_SN172_0451_BD26VHACXX_Merkenschlager/Unaligned/Sample_3InpVS/3InpVS_ACAGTG_L003_R1_001.fastq.gz"
#baseName = "/csc/rawdata/Dillon/DillonTest/test"
fastq = sys.argv[1]
baseName = sys.argv[2]
genome = sys.argv[3]
outputPath = sys.argv[4]

saiOut = os.path.join(outputPath,baseName+".sai")
trimmedFQOut = os.path.join(outputPath,baseName+"trimmed.fq.gz")

print os.environ["LOADEDMODULES"]

if not os.path.isfile(genomeFastaFiles[genome]) or not os.path.isfile(genomeFastaFiles[genome]+".bwt") or not os.path.isfile(genomeFastaFiles[genome]+".sa"):
  if os.path.isfile(genomeFastaFiles[genome]): 
    print "Not all necessary index files found..indexing"
    #p = subprocess.Popen(["/bin/bash",'-i',"-c","bwa index -a bwtsw "+genome], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #stdout,stderr = p.communicate()
  else:
    "Fasta file is not found"
elif os.path.isfile(genomeFastaFiles[genome]) and os.path.isfile(genomeFastaFiles[genome]+".bwt") and os.path.isfile(genomeFastaFiles[genome]+".sa"):
  if not os.path.isfile(saiOut):
    pairedAlignCMD1 = "zcat "+fastq+" | python  /csc/rawdata/Cscbioinf/bioinfResources/trimFQ.py 50 | gzip - > "+trimmedFQOut
    print pairedAlignCMD1
    p = subprocess.Popen(["/bin/bash",'-i',"-c",pairedAlignCMD1], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()
    pairedAlignCMD2 = "bwa aln -t 8 "+genomeFastaFiles[genome]+" "+trimmedFQOut+" > "+saiOut
    print pairedAlignCMD2
    p = subprocess.Popen(["/bin/bash",'-i',"-c",pairedAlignCMD2], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = p.communicate()

