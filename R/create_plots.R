## create plots and visualisations using R
# - vertex degree distribution
# - minimum distance distribution
# - boxplot of cooc values distribution for each corpus

setwd("../python/IRGraphProject/data/results")
load(".RData")
require(ggplot2)
require(gridExtra)
require(xtable)

# vertex degree
wen_vdeg <- read.csv("cooc_wiki_en/v_degree_hist.csv", sep=",", header = FALSE )
wen_vdeg <- as.data.frame(t(wen_vdeg))
names(wen_vdeg) <- c("vertexdegree","count")
head(wen_vdeg,10)

wsi_vdeg <- read.csv("cooc_wiki_sim/v_degree_hist.csv", sep=",", header = FALSE )
wsi_vdeg <- as.data.frame(t(wsi_vdeg))
names(wsi_vdeg) <- c("vertexdegree","count")
head(wsi_vdeg,10)

nl_vdeg <- read.csv("cooc_nl/v_degree_hist.csv", sep=",", header = FALSE )
nl_vdeg <- as.data.frame(t(nl_vdeg))
names(nl_vdeg) <- c("vertexdegree","count")
head(nl_vdeg,10)

den_vdeg <- read.csv("cooc_denews10k/v_degree_hist.csv", sep=",", header = FALSE )
den_vdeg <- as.data.frame(t(den_vdeg))
names(den_vdeg) <- c("vertexdegree","count")
head(den_vdeg,10)

col1 = "#56B4E9"
q1 <- ggplot(wsi_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("Wiki simple") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") + 
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,11000)) + scale_x_continuous(limits = c(0,6000))
q2 <- ggplot(wen_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("Wiki english") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") +
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,11000)) + scale_x_continuous(limits = c(0,6000))
q3 <- ggplot(nl_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("Nachrichtenleicht") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") +
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,1500)) + scale_x_continuous(limits = c(0,300))
q4 <- ggplot(den_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("denews10k") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") +
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,1500)) + scale_x_continuous(limits = c(0,300))

pdf("vdeg_plots.pdf",width=10,height=10)
grid.arrange(q1,q2,q3,q4,nrow=2,ncol=2)
dev.off()

# minimum distance
# histograms
wen_mdh <- read.csv("cooc_wiki_en/min_dist_hist.csv", sep=",", header = FALSE )
wen_mdh <- as.data.frame(t(wen_mdh))
names(wen_mdh) <- c("min.distance","count")
wen_mdh$min.distance <- as.factor(wen_mdh$min.distance)
wen_mdh

wsi_mdh <- read.csv("cooc_wiki_sim/min_dist_hist.csv", sep=",", header = FALSE )
wsi_mdh <- as.data.frame(t(wsi_mdh))
names(wsi_mdh) <- c("min.distance","count")
wsi_mdh$min.distance <- as.factor(wsi_mdh$min.distance)
wsi_mdh

den_mdh <- read.csv("cooc_denews10k/min_dist_hist.csv", sep=",", header = FALSE )
den_mdh <- as.data.frame(t(den_mdh))
names(den_mdh) <- c("min.distance","count")
den_mdh$min.distance <- as.factor(den_mdh$min.distance)
den_mdh

nl_mdh <- read.csv("cooc_nl/min_dist_hist.csv", sep=",", header = FALSE )
nl_mdh <- as.data.frame(t(nl_mdh))
names(nl_mdh) <- c("min.distance","count")
nl_mdh$min.distance <- as.factor(nl_mdh$min.distance)
nl_mdh

q5 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=wsi_mdh[wsi_mdh$count > 0,], log="y") + ggtitle("Wiki simple")
q6 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=wen_mdh[wen_mdh$count > 0,], log="y") + ggtitle("Wiki english")
q7 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=nl_mdh[nl_mdh$count > 0,], log="y") + ggtitle("Nachrichtenleicht")
q8 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=den_mdh[den_mdh$count > 0,], log="y") + ggtitle("denews10k")

pdf("mdh_plots.pdf")
grid.arrange(q5,q6,q7,q8,nrow=2,ncol=2)
dev.off()

# percentage
# table 2
# "Anteil der Weglängen paarweiser kürzester Wege zwischen  
# allen Knoten, in Prozent"

table2 <- merge(nl_mdh,den_mdh, by="min.distance",all.y=TRUE)
tmp <- merge(wsi_mdh,wen_mdh, by="min.distance")
table2 <- merge(table2,tmp,by="min.distance")
rm(tmp)
names(table2) <- c("min.distance","nl","denews10k","wiki_sim","wiki_en")
row.names(table2) <- table2$min.distance
table2 <- table2[,-1] # remove column
# calculate col sums
colSums(table2)
table2 <- rbind(table2, colSums(table2))
row.names(table2) <- c(row.names(table2)[-11],"sum")

# divide each cell by sum
a <- apply(table2,1,function(x) x*100 / table2["sum",])
# results to dataframe
table2 <- do.call(rbind.data.frame, a)
rm(a)

table2_table_t <- xtable(t(table2)[,c(-1,-11)])
table2_tablet <- xtable(table2[-1,])



# cooccurrence values
nms <- c("w1","w2","sig")

wsi_coo <- read.csv("../cooc_wiki_sim.csv", sep=",", header = FALSE)
names(wsi_coo) <- nms
wsi_coo[wsi_coo$sig < 0,]

wen_coo <- read.csv("../cooc_wiki_en.csv", sep=",", header = FALSE )
names(wen_coo) <- nms
wen_coo[wen_coo$sig < 0,]

nl_coo <- read.csv("../cooc_nl.csv", sep=",", header = FALSE )
names(nl_coo) <- nms
nl_coo[nl_coo$sig < 0,]

den_coo <- read.csv("../cooc_denews10k.csv", sep=",", header = FALSE )
names(den_coo) <- nms
den_coo[den_coo$sig < 0,]
den_coo[den_coo$sig < -50,]

# reshape data
wsi_coo$id <- "wsi"
wen_coo$id <- "wen"
nl_coo$id <- "nl"
den_coo$id <- "den"

tst <- rbind(nl_coo[3:4],den_coo[3:4],wen_coo[3:4],wsi_coo[3:4])
tst$id <- as.factor(tst$id)

#boxplot
qplot(id, sig, data=tst, geom="boxplot")
# log poxplot
qplot(id, sig, data=tst, geom="boxplot", log="y")
