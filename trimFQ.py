import sys
TrimTo = int(sys.argv[1])
sys.path.append('/csc/rawdata/Cscbioinf/bioinfResources/lib/python2.7/site-packages/biopython-1.64-py2.7-linux-x86_64.egg/')
from Bio.SeqIO.QualityIO import FastqGeneralIterator
trim = TrimTo
#handle = open(FQTrimed, "w")
write = sys.stdout.write
for title, seq, qual in FastqGeneralIterator(sys.stdin) :
    write("@%s\n%s\n+\n%s\n" % (title, seq[:trim], qual[:trim]))        