require(GEOquery)
require(SRAdb)
geoID <- args[1] 

sqlfile <- getSRAdbFile()
sra_con <- dbConnect(SQLite(),sqlfile)


sraList <- vector("character")
geoID <- "GSE53595"

gqRes <- getGEO(geoID)

if(class(gqRes) == "list"){
  for(i in 1:length(gqRes)){
  sraUnparsed <- pData(gqRes[[i]])$relation.1
  sraList <- c(sraList,gsub(".*term=","",sraUnparsed))
  }
}
rs = listSRAfile(sraList, sra_con, fileType = "fastq")

FirstSet <- cbind(as.vector(phenoData(gqRes[[1]])@data$title),basename(as.vector(phenoData(gqRes[[1]])@data$supplementary_file_2)))
SecondSet <- cbind(as.vector(phenoData(gqRes[[2]])@data$title),basename(as.vector(phenoData(gqRes[[2]])@data$supplementary_file_2)))
AllSet <- rbind(FirstSet,SecondSet)
SamplesToMerge <- rs[,c("experiment","run")]
moreSamples <- merge(SamplesToMerge,AllSet,by.x=1,by.y=2)
GSM1296532
GSM1296533
GSM1296534  
GSM1296535
GSM1296538
GSM1296550 
GSM1296544  
GSM1296551


wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR500/SRR500161/SRR500161.fastq.gz ./
wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR500/SRR500162/SRR500162.fastq.gz ./
  wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR500/SRR500163/SRR500163.fastq.gz ./ &
  wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR500/SRR500164/SRR500164.fastq.gz ./ &
  wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR500/SRR500165/SRR500165.fastq.gz ./ &
  wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR500/SRR500166/SRR500166.fastq.gz ./ &
  wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR500/SRR500167/SRR500167.fastq.gz ./ &
  
  
  
  
  