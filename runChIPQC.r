library(ChIPQC)
Arguments <- commandArgs(trailingOnly = T)

bamFile <- Arguments[1]
organism <- Arguments[2]
blkList <- Arguments[3]
if(organism == "mm9"){
  chromosomes=c("chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chrX","chrY")
}else{
  chromosomes=NULL
}

chipout <- file.path(dirname(dirname(bamFile)),"chipqc",gsub("\\.bam","\\.RData",basename(bamFile)))
#chromosomes <- c("chr19")
qc <- ChIPQCsample(bamFile,blacklist=blkList,annotation=organism,chromosomes=chromosomes)
save(qc,file=chipout)
#ChIPQCreport(reportName="ChIPQC",reportFolder=gsub("\\.bam","_ChIPQC",bamFile))
