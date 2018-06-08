#More playing around with graphs in ggplot2

#DATA
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
  #materialData$Material  <- as.character(materialData$Material)
  #materialData$Material[(materialData$Material == "Wood" & materialData$BuildingArea==612550.139774)| (materialData$Material == "Wood" & materialData$BuildingArea== 868800.5559) ] <- "No Data"
  materialData$Material2  <- as.character(materialData$Material)
  materialData$Material2[materialData$Material == "No_Data"] <- "No Data"
  landuseData$LandUse2  <- as.character(landuseData$LandUse)
  landuseData$LandUse2[landuseData$LandUse == "No_Data"] <- "No Data"


#Stacked barplot with multiple groups: 
#MATERIALS
  blanktheme <- theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank(), axis.line = element_line(colour = "black"))
  materialplot <- ggplot(data=materialData, aes(x=Period2, y=Area, fill=Material2))
  materials <- scale_fill_manual(values=c("#cc0000", "#999999", "#ffe680"))
  title <- ggtitle("Building Materials Through Time", subtitle = NULL)
  xlabel <- xlab("Time Period")
  ylabel <- ylab("Area (sqft)")
  bars <- geom_bar(stat="identity",color="black")
  yscale <- scale_y_continuous(labels = comma)
  Mcolors <- scale_fill_manual(values = c("#cc0000","#ffffff", "#999999", "#ffe680"))
  tufte <- theme_tufte(ticks=FALSE)
  legendM <- labs(fill='Material')

#LAND USE
  blanktheme <- theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),panel.background = element_blank(), axis.line = element_line(colour = "black"))
  landuseplot <- ggplot(data=landuseData, aes(x=Period2, y=Area, fill=LandUse2))
  landuse <- scale_fill_manual(values=c("#f13026","#a72cf4","#4286f4", "#f2f226"))
  Mcolors <- scale_fill_manual(values = c("#f13026","#a72cf4","#ffffff","#4286f4", "#f2f226"))
  title <- ggtitle("Building Uses Through Time", subtitle = NULL)
  xlabel <- xlab("Time Period")
  ylabel <- ylab("Area (sqft)")
  bars <- geom_bar(stat="identity",color="black")
  yscale <- scale_y_continuous(labels = comma)
  tufte <- theme_tufte(ticks=FALSE)
  legendL <- labs(fill='Land Use')

#create stacked bar charts
  materialsgraph <- materialplot+bars+blanktheme+yscale+xlabel+ylabel+title+tufte+Mcolors+legendM
  landusegraph <- landuseplot+bars+blanktheme+yscale+xlabel+ylabel+title+tufte+Mcolors+legendL

#Export as high res tiff
  tiff('LandUsePlot.tiff', units="in", width=5, height=5, res=300)
  landusegraph
  dev.off()

#Export to illustrator(don't know if this is high res or not yet)
  pdf('Orig_Mat.pdf', width=6, height=6)
  graph
  dev.off()



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









  

