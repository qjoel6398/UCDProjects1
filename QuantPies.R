quantT <- read.csv(file="Quant.csv", header=TRUE, sep=",")

#Subset dataframe and change column name
Orig_material<-quantT[13:15,c("X","Original")]
colnames(Orig_material)[1] <- "Material"


Pre_material<-quantT[13:15,c("X","PreWW2")]
col <- colnames(trSamp) <- "newname2"
Post_material<-quantT[13:15,c("X","PostWW2")]
colnames(trSamp) <- "newname2"
Cont_material<-quantT[13:15,c("X","Contemporary")]
colnames(trSamp) <- "newname2"

Orig_landuse<-quantT[17:19,c("X","Original")]
colnames(trSamp) <- "newname2"
Pre_landuse<-quantT[17:19,c("X","PreWW2")]
colnames(trSamp) <- "newname2"
Post_landuse<-quantT[17:19,c("X","PostWW2")]
colnames(trSamp) <- "newname2"
Cont_landuse<-quantT[17:19,c("X","Contemporary")]
colnames(trSamp) <- "newname2"


#PIE CHARTs
library(ggplot2)

#barplot
bp<- ggplot(Orig_material, aes(x="", y=Original, fill=Material))+ geom_bar(width = 1, stat = "identity")
#+ labs(x="", y="Building Material",fill = Material)
bp

#normal pie chart
pie <- bp + coord_polar("y", start=0)
pie

##manual color fill
#materials
materials<-scale_fill_manual(values=c("#cc0000", "#999999", "#ffe680"))

#create blank theme
blank_theme <- theme_minimal()+
  theme(
    axis.title.x = element_blank(),
    axis.title.y = element_blank(),
    panel.border = element_blank(),
    panel.grid=element_blank(),
    axis.ticks = element_blank(),
    plot.title=element_text(size=14, face="bold")
  )

#format percentages:
percent <- function(x, digits = 2, format = "f", ...) {
  paste0(formatC(100 * x, format = format, digits = digits, ...), "%")
}

##labels
#labels<-geom_text(aes(y = Original/3 + c(0, cumsum(Original)[-length(Original)]),label = percent(Original/100)), size=5)
labels<-geom_text(aes(y=Original,label=percent(Original)), size=5)
labels<-geom_text(aes(y = Original/3 + c(0, cumsum(Original)[-length(Original)]),label=percent(Original)), size=5)



#styled pie chart
pie = pie + materials + blank_theme + theme(axis.text.x=element_blank()) 
pie



#Export as high res tiff
tiff('Orig_Mat.tiff', units="in", width=5, height=5, res=300)
pie
dev.off()

#Export to illustrator(don't know if this is high res or not yet)
#Remember, you can always "Zoom" your plots in R studio to see the whole thing. Damn!
pdf('Orig_Mat.pdf', units="in", width=4, height=4, res=300)
pie
dev.off()



  

