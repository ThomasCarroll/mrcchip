#!/usr/bin/python -O

import subprocess                                                 
import os                                                         
import sys                                                        


def module_add(modulename):
  p = subprocess.Popen("/usr/bin/modulecmd python add "+modulename, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
  stdout,stderr = p.communicate()
  exec stdout


csvFile = sys.argv[1]
genome = sys.argv[2]
baseDir = sys.argv[3]


#blacklist = {"mm9":"/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9-blacklist.bed"}


module_add("R/3.1.0")


chipqccmd = "Rscript /csc/rawdata/Cscbioinf/bioinfResources/chippipeline/poolResults.r "+csvFile+" "+genome+" "+baseDir
print chipqccmd
p = subprocess.Popen(["/bin/bash",'-i',"-c",chipqccmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout,stderr = p.communicate()
