
# library
library(multcompView)

# Create data
TAP_SPI <- read.csv(file="TAP_SPI.csv", header=TRUE, sep=",")


# What is the effect of the treatment on the value ?

fit <- aov(sample$Count_~sample$TSEGNAME, data = sample)


# Tukey test to study each pair of treatment :
tukey3 <- TukeyHSD(fit, 'sample$TSEGNAME', conf.level=0.95)


# Tukey test representation :
plot(tukey3 , las=1 , col="brown" )


# I need to group the treatments that are not different each other together.
generate_label_df <- function(tukey3, variable){
  
  # Extract labels and factor levels from Tukey post-hoc 
  Tukey.levels <- TUKEY[[variable]][,4]
  Tukey.labels <- data.frame(multcompLetters(Tukey.levels)['Letters'])
  
  #I need to put the labels in the same order as in the boxplot :
  Tukey.labels$TSEGNAME=rownames(Tukey.labels)
  Tukey.labels=Tukey.labels[order(Tukey.labels$TSEGNAME) , ]
  return(Tukey.labels)
}

# Apply the function on my dataset
LABELS=generate_label_df(tukey3 , 'sample$TSEGNAME')


# A panel of colors to draw each group with the same color :
my_colors=c( rgb(143,199,74,maxColorValue = 255),rgb(242,104,34,maxColorValue = 255), rgb(111,145,202,maxColorValue = 255),rgb(254,188,18,maxColorValue = 255) , rgb(74,132,54,maxColorValue = 255),rgb(236,33,39,maxColorValue = 255),rgb(165,103,40,maxColorValue = 255))

# Draw the basic boxplot
a=boxplot(sample$Count_ ~ sample$TSEGNAME , ylim=c(min(sample$Count_) , .1*max(sample$Count_)) , ylab="counts" , main="" )

# I want to write the letter over each box. Over is how high I want to write it.
over=0.1*max( a$stats[nrow(a$stats),] )

#Add the labels
text( c(1:nlevels(data$treatment)) , a$stats[nrow(a$stats),]+over , LABELS[,1]  , col=my_colors[as.numeric(LABELS[,1])] )
