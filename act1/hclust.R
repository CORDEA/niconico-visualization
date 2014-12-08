# Author: Yoshihiro Tanaka
# date  : 2014-11-25
library(amap)
library(cluster)
library(ctc)

infile <- read.table("animes_tag.tsv", sep='\t', header=F, skip=1)
rownames(infile) <- infile[,1]
infile <- infile[,-1]
matrix <- as.data.frame(infile)
matrix.d <- Dist(matrix, method="euclidean")
hc.d <- hclust(matrix.d)
write.table(hc2Newick(hc.d), file="newick.txt",row.names=FALSE,col.names=FALSE)
