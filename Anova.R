
#Set working directory and read in csv
setwd("C:\Users\qjoel\OneDrive\Desktop\GEOM\R")
TAP_SPI <- read.csv(file="TAP_SPI.csv", header=TRUE, sep=",")

#Sampling
treatment <- subset(TAP_SPI,Count_!=0,select = c(ID,TSEGNAME,Count_,Sum_TT_Gra,Sum_DT_Gra,Sum_CT_Gra))
controlsub <- subset(TAP_SPI,Count_==0,select = c(ID,TSEGNAME,Count_,Sum_TT_Gra,Sum_DT_Gra,Sum_CT_Gra))
control<-controlsub[sample(nrow(controlsub),4000,replace=FALSE),]
sample = rbind(treatment,control)

#Description
install.packages(dplyr)
library(dplyr)
install.packages(ggplot2)
library(ggplot2)
description<-group_by(sample, TSEGNAME) %>%
  summarise(
    count = n()
  )
sample$TSEGNAME <- reorder(sample$TSEGNAME, sample$Count_)

description

#make group to use in plots, tests
segments<- factor(sample$TSEGNAME)
group <- reorder(sample$TSEGNAME, sample$Count_)
counts<-sample$Count_


#Check assumptions:
##Observations independent from segment groups? As far as I know, yes.
##Are observation groups normally distributed?


#qqnorm(level);qqline(level, col = 2)
facet<-ggplot(sample,aes(x=Count_))+geom_histogram(color="black",fill="white",stat = "count")+facet_grid(TSEGNAME~.)
facet<-ggplot(sample,aes(x=Count_))+geom_histogram()+facet_grid(TSEGNAME~.)+theme_bw()
histogram<-ggplot(sample,aes(x=levels[7]))+geom_histogram(bin = "",stat = "count")

##Do those distrubutions have a common variance? (Levene's test)
install.packages(Rcmdr)
library(Rcmdr)
equal<-leveneTest(sample$Count_, group)
#to get p values out of levenes test list :
attributes(equal)
equal

#plot data
graph1 <- ggplot(sample, aes(counts,group))+geom_point((aes(color = counts)))+geom_smooth(method='lm')
graph2 <- qplot(counts,group,color = counts, data=sample,geom="point" )
graph1
graph2

histogram
#ANOVA
fit <- aov(sample$Count_~sample$TSEGNAME, data = sample)
summary(fit)
model.tables(fit)

#Tukey Test
tukey<-TukeyHSD(fit)
tukey<-data.frame(TukeyHSD(fit))












Ok, 


