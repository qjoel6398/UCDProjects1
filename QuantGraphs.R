materialData <- read.csv(file="Material3.csv", header=TRUE, sep=",")
landuseData <- read.csv(file="Landuse3.csv", header=TRUE, sep=",")



#Bar Charts
library(ggplot2)
library(scales)
library(ggthemes)


head(materialData)

#Reorder levels in factor to order the bars of the barchart.
materialData$Period2 <- factor(materialData$Period, levels = c("Original","PreWW2","PostWW2","Contemporary"))
landuseData$Period2 <- factor(landuseData$Period, levels = c("Original","PreWW2","PostWW2","Contemporary"))

#Creating empty bars
#materialData$Material  = as.character(materialData$Material)
#materialData$Material[(materialData$Material == "Wood" & materialData$BuildingArea==612550.139774)| (materialData$Material == "Wood" & materialData$BuildingArea== 868800.5559) ] = "No Data"
materialData$Material2  = as.character(materialData$Material)
materialData$Material2[materialData$Material == "No_Data"] = "No Data"


landuseData$LandUse2  = as.character(landuseData$LandUse)
landuseData$LandUse2[landuseData$LandUse == "No_Data"] = "No Data"


# Stacked barplot with multiple groups: MATERIALS
blanktheme<-theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank(), axis.line = element_line(colour = "black"))
materialplot<-ggplot(data=materialData, aes(x=Period2, y=Area, fill=Material2))
materials<-scale_fill_manual(values=c("#cc0000", "#999999", "#ffe680"))
title<-ggtitle("Building Materials Through Time", subtitle = NULL)
xlabel<-xlab("Time Period")
ylabel<-ylab("Area (sqft)")
bars<-geom_bar(stat="identity",color="black")
yscale<-scale_y_continuous(labels = comma)
Mcolors<- scale_fill_manual(values = c("#cc0000","#ffffff", "#999999", "#ffe680"))
tufte <- theme_tufte(ticks=FALSE)
legendM<- labs(fill='Material')



#LAND USE
blanktheme<-theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank(), axis.line = element_line(colour = "black"))
landuseplot<-ggplot(data=landuseData, aes(x=Period2, y=Area, fill=LandUse2))
landuse<-scale_fill_manual(values=c("#f13026","#a72cf4","#4286f4", "#f2f226"))
Mcolors<- scale_fill_manual(values = c("#f13026","#a72cf4","#ffffff","#4286f4", "#f2f226"))
title<-ggtitle("Building Uses Through Time", subtitle = NULL)
xlabel<-xlab("Time Period")
ylabel<-ylab("Area (sqft)")
bars<-geom_bar(stat="identity",color="black")
yscale<-scale_y_continuous(labels = comma)
tufte <- theme_tufte(ticks=FALSE)
legendL<- labs(fill='Land Use')


materialsgraph<-materialplot+bars+blanktheme+yscale+xlabel+ylabel+title+tufte+Mcolors+legendM

landusegraph<-landuseplot+bars+blanktheme+yscale+xlabel+ylabel+title+tufte+Mcolors+legendL









#Export as high res tiff
tiff('LandUsePlot.tiff', units="in", width=5, height=5, res=300)
landusegraph
dev.off()

#Export to illustrator(don't know if this is high res or not yet)
#Remember, you can always "Zoom" your plots in R studio to see the whole thing. Damn!
pdf('Orig_Mat.pdf', width=6, height=6)
graph
dev.off()



  

