library(ChIPQC)
Arguments <- commandArgs(trailingOnly = T)
bamFile <- "/csc/analysis/Cscbioinf/IkarosRelated2/AlignedData/Ebf1DupMarked.bam"
bamFile <- Arguments[1]
res <- file.path(dirname(dirname(bamFile)),"chipqc",gsub(".bam",".RData",basename(bamFile)))
load(res)          


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
exportNormalisedBW(bamFile,qc)
