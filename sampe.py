#!/usr/bin/python -O
#PBS -N myjob
#PBS -l select=1:ncpus=1:mem=12GB
#PBS -l walltime=70:00:00

import subprocess                                                 
import os                                                         
import sys                                                        

def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout

module_add("bio-bwa/0.7.5a")
module_add("samtools/0.1.18")

genomeFastaFiles = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9.fa"}
#genome = "mm9"
#fastq = "/csc/rawdata/Merkenshlager/131209_SN172_0451_BD26VHACXX_Merkenschlager/Unaligned/Sample_3InpVS/3InpVS_ACAGTG_L003_R1_001.fastq.gz"
#baseName = "/csc/rawdata/Dillon/DillonTest/test"
fastq = sys.argv[1]
baseName = sys.argv[2]
genome = sys.argv[3]
outputPath = sys.argv[4]

#fastq1,fastq2 = fastq.split(",")
sam = os.path.join(outputPath,baseName+".sam")
bam = os.path.join(outputPath,baseName+"")
saiRead1 = os.path.join(outputPath,baseName+"read1.sai")
saiRead2 = os.path.join(outputPath,baseName+"read2.sai")
fastq1 = os.path.join(outputPath,baseName+"read1trimmed.fq.gz")
fastq2 = os.path.join(outputPath,baseName+"read2trimmed.fq.gz")
if not os.path.isfile(sam):
  pairedAlignCMD = "bwa sampe "+genomeFastaFiles[genome]+" "+saiRead1+" "+saiRead2+" "+fastq1+" "+fastq2+" > "+sam
  print pairedAlignCMD
  p = subprocess.Popen(["/bin/bash",'-i',"-c",pairedAlignCMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
if not os.path.isfile(bam+".bam"):
  sortCMD = "samtools view -Sb "+sam+" | samtools sort -m 8000000000 - "+bam
  print sortCMD
  p = subprocess.Popen(["/bin/bash",'-i',"-c",sortCMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
  indexCMD = "samtools index "+bam+".bam"
  print indexCMD
  p = subprocess.Popen(["/bin/bash",'-i',"-c",indexCMD], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  stdout,stderr = p.communicate()
  