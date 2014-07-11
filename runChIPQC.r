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
exportNormalisedBW <- function(bamFile,qc,normaliseTo="blacklisted"){
  require(GenomicAlignments)
  require(rtracklayer)
  #library(QuasR)
  extendBy <- fragmentlength(qc)
  message("Reading tags from ",bamFile,appendLF=FALSE)
  #totalReads <- alignmentStats(bamFile)[,"mapped"]
  if(normaliseTo == "blacklisted"){
    totalReads <- qc@FlagAndTagCounts["MapQPass"] - qc@CountsInFeatures$BlackList
  }
  if(normaliseTo == "Total"){
    totalReads <- qc@FlagAndTagCounts["Mapped"]
  }  
  if(normaliseTo == "UniqueTotal"){
    totalReads <- qc@FlagAndTagCounts["Mapped"]-qc@FlagAndTagCounts["Duplicates"]
  }  
  total <- readGAlignmentsFromBam(bamFile)
  message("..done")
  message("Read in ",length(total)," reads")
  message("Extending reads to fragmentlength of ",extendBy," ..",appendLF=FALSE)
  temp <- resize(as(total,"GRanges"),extendBy,"start")
  message("..done")
  rm(total)
  gc()
  message("Calculating coverage..",appendLF=FALSE)
  genomeCov <- coverage(temp)
  rm(temp)
  message("..done")
  
  message("Normalised coverage..",appendLF=FALSE)
  genomeCov <- (genomeCov/totalReads)*1000000
  message("..done")
  message("Exporting coverage..",appendLF=FALSE)
  export.bw(genomeCov,file.path(dirname(dirname(bamFile)),"CoveragePileup/",gsub("\\.bam","Normalised\\.bw",basename(bamFile))))
  message("..done")
}

