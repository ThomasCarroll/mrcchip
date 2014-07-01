library(ChIPQC)
baseDir <- "/csc/analysis/Cscbioinf/2014020_sSauer_Extra/"
SampleSheet <- "/csc/analysis/Cscbioinf/2014020_sSauer_Extra/chipsSauer3.csv"
organism <- "mm9"
Arguments <- commandArgs(trailingOnly = T)


SampleSheet <- Arguments[1]
organism <- Arguments[2]
baseDir <- Arguments[3]

ss <- read.delim(SampleSheet,sep="\t",header=F)

if(organism == "mm9"){
  chromosomes=c("chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chrX","chrY")
  blklist <- "/csc/rawdata/Cscbioinf/bioinfResources/mm9/mm9-blacklist.bed"
}else{
  blklist <- NULL
  chromosomes=NULL
  
}


bamFiles <- dir(file.path(baseDir,"AlignedData"),pattern="*.DupMarked\\.bam$",full.name=T)
bamBase <- gsub("DupMarked\\.bam","",basename(bamFiles))
bamFrame <- cbind(bamBase,bamFiles)


peaks <-  dir(file.path(baseDir,"AlignedData"),pattern="*_peaks.bed$",full.name=T)
peaksBase <- gsub("_WithInput.*","",basename(peaks))
peakFrame <- cbind(peaksBase,peaks)

ss <- ss[ss[,11] == "Report",]

ssFrame <- merge(ss[,c(2,4,6,7,8,9,10,11)]
                 ,merge(bamFrame,peakFrame,by=1,all.x=T,all.y=F)
                 ,by=1,all.x=F,all.y=F)

bamControl <- vector("character",length=nrow(ssFrame))
for(i in 1:nrow(ssFrame)){
  if(any(ssFrame[,1] %in% ssFrame[i,2])){
    bamControl[i] <- as.vector(ssFrame[ssFrame[,1] %in% ssFrame[i,2],9])
  }else{
    bamControl[i] <- NA
  }
}


#for(k in 1:length(bamFiles)){
#  cat("Processing sample ",bamFiles[k])
#  listOfRes[[k]] <- ChIPQCsample(bamFiles[k],peaks=peaks[k],blacklist=blklist,annotation="mm9")
#}

#names(listOfRes) <- gsub("\\.sorted\\.bam","",basename(bamFiles))


SS2 <- data.frame(
  SampleID=as.vector(ssFrame[,1]),
  Tissue=as.vector(ssFrame[,3]),
  Factor=as.vector(ssFrame[,4]),
  Condition=as.vector(ssFrame[,5]),
  Treatment=as.vector(ssFrame[,6]),
  Replicate=as.vector(ssFrame[,7]),
  bamReads=as.vector(ssFrame[,9]),
  bamControl=bamControl,
  ControlID=as.vector(ssFrame[,2]),
  Peaks=as.vector(ssFrame[,10]),
  PeakCaller=c(rep("macs",nrow(ssFrame)))
  #Peaks=c(rep(NA,7))
)


resExperiment <- ChIPQC(SS2,annotation=organism,blacklist=blklist,chromosomes=chromosomes)
save(resExperiment,file=file.path(baseDir,paste0(gsub("\\..*$","",basename(SampleSheet)),"_report.RData")))
