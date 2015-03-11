## create plots and visualisations using R
# - vertex degree distribution
# - minimum distance distribution

setwd("../python/IRGraphProject/data/results")
require(ggplot2)
require(gridExtra)

# vertex degree
wen_vdeg <- read.csv("cooc_wiki_en/v_degree_hist.csv", sep=",", header = FALSE )
wsi_vdeg <- read.csv("cooc_wiki_sim/v_degree_hist.csv", sep=",", header = FALSE )
nl_vdeg <- read.csv("cooc_nl/v_degree_hist.csv", sep=",", header = FALSE )
den_vdeg <- read.csv("cooc_denews10k/v_degree_hist.csv", sep=",", header = FALSE )

wen_vdeg <- as.data.frame(t(wen_vdeg))
names(wen_vdeg) <- c("vertexdegree","count")
head(wen_vdeg,10)

wsi_vdeg <- as.data.frame(t(wsi_vdeg))
names(wsi_vdeg) <- c("vertexdegree","count")
head(wsi_vdeg,10)

nl_vdeg <- as.data.frame(t(nl_vdeg))
names(nl_vdeg) <- c("vertexdegree","count")
head(nl_vdeg,10)

den_vdeg <- as.data.frame(t(den_vdeg))
names(den_vdeg) <- c("vertexdegree","count")
head(den_vdeg,10)

col1 = "#56B4E9"
q1 <- ggplot(wsi_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("Wiki simple") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") + 
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,10000)) #+ scale_x_continuous(limits = c(0,100))
q2 <- ggplot(wen_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("Wiki english") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") +
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,10000)) #+ scale_x_continuous(limits = c(0,100))
q3 <- ggplot(nl_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("Nachrichtenleicht") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") +
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,1000)) + scale_x_continuous(limits = c(0,120))
q4 <- ggplot(den_vdeg, aes(x=vertexdegree, y=count)) + ggtitle("denews10k") + 
  geom_point(shape=19, color = col1, alpha = 0.3) + xlab("Knotengrad") +
  scale_y_continuous(name ="Anzahl Knoten", limits = c(0,1000)) + scale_x_continuous(limits = c(0,120))

pdf("vdeg_plots.pdf",width=10,height=10)
grid.arrange(q1,q2,q3,q4,nrow=2,ncol=2)
dev.off()

# minimum distance
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

q1 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=wsi_mdh[wsi_mdh$count > 0,], log="y") + ggtitle("Wiki simple")
q2 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=wen_mdh[wen_mdh$count > 0,], log="y") + ggtitle("Wiki english")
q3 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=nl_mdh[nl_mdh$count > 0,], log="y") + ggtitle("Nachrichtenleicht")
q4 <- qplot(min.distance, count, geom="bar", stat="identity", xlab="min. Distanz", ylab="Anzahl Knoten", 
      data=den_mdh[den_mdh$count > 0,], log="y") + ggtitle("denews10k")

pdf("mdh_plots.pdf")
grid.arrange(q1,q2,q3,q4,nrow=2,ncol=2)
dev.off()
