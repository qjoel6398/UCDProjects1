library(dplyr)
#May not need this^
library(ggplot2)
library(data.table)

TAP_SPI <- read.csv(file="TAP_SPI.csv", header=TRUE, sep=",")
TAP_SPI2 <- TAP_SPI[c("TSEGNAME","Count_")]
write.csv(TAP_SPI2, file = "TAP_SPI2.csv")


###############Create Control and treatment group
treatment <- subset(TAP_SPI,Count_!=0,select = c(ID,TSEGNAME,Count_,Sum_TT_Gra,Sum_DT_Gra,Sum_CT_Gra))
controlsub <- subset(TAP_SPI,Count_==0,select = c(ID,TSEGNAME,Count_,Sum_TT_Gra,Sum_DT_Gra,Sum_CT_Gra))
control<-controlsub[sample(nrow(controlsub),4000,replace=FALSE),]
sample = rbind(treatment,control)



###############Description of data
#Table
tap_spi_dt <- data.table(TAP_SPI)
tap_spidescribe = tap_spi_dt[,list(mean=mean(Count_),sd=sd(Count_), sum = sum(Count_)),by=TSEGNAME]
#Plot
tap_spiplotmean <- ggplot(tap_spidescribe, aes(mean, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)
tap_spiplotsum <- ggplot(tap_spidescribe, aes(sum, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)

#Table
sampledt <- data.table(sample)
describesample = sampledt[,list(mean=mean(Count_),sd=sd(Count_), sum = sum(Count_)),by=TSEGNAME]
#Plot
sampleplotmean <- ggplot(describesample, aes(mean, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)
sampleplotsum <- ggplot(describesample, aes(sum, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)
#Histogram
samplehistfacet <- ggplot(sample, aes(x=Count_)) + geom_histogram(binwidth=1,color="black", fill="white") + xlab("Number of customers in Tapestry Segment") + facet_wrap(~TSEGNAME)

#Table
treatmentdt <- data.table(treatment)
describetreatment = treatmentdt[,list(mean=mean(Count_),sd=sd(Count_), sum = sum(Count_)),by=TSEGNAME]
#Plot
treatmentplotmean <- ggplot(describetreatment, aes(mean, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)
treatmentplotsum <- ggplot(describetreatment, aes(mean, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)
#Histogram
TreatmenthistFacet <- ggplot(treatment, aes(x=Count_)) + geom_histogram(binwidth=1,color="black", fill="white") + xlab("Number of customers in Tapestry Segment") + facet_wrap(~TSEGNAME)

#Table
controldt <- data.table(control)
describecontrol = controldt[,list(mean=mean(Count_),sd=sd(Count_), sum = sum(Count_)),by=TSEGNAME]
#Plot
controlplotmean <- ggplot(describecontrol, aes(mean, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)
controlplotsum <- ggplot(describecontrol, aes(mean, TSEGNAME)) + geom_point() + stat_summary(fun.data = "mean_cl_boot", colour = "red", size = 2)
#Histogram

#single segment description
attach(treatment$TSEGNAME)
UrbanChic <- subset(sample,TSEGNAME=="Urban Chic",select = c(ID,TSEGNAME,Count_,Sum_TT_Gra,Sum_DT_Gra,Sum_CT_Gra))
UrbHist <- ggplot(UrbanChic, aes(x=Count_)) + geom_histogram(binwidth=1,color="black", fill="white") + xlab("Number of customers in Tapestry Segment")
detach(treatment$TSEGNAME)


#####################IS OUR DATA NORMAL? NO
normality <- with(sample, tapply(sample$Count_,sample$TSEGNAME, shapiro.test))
normalityPs <- sapply(normality, `[`, c("p.value"))
normalityPsDf <- data.frame(normalityPs)
normalityPsDf$segment <- names(normalityPsDf)
normalityPsDf$segment <- names(normalityPsDf)
normalityPsDfTran <- transpose(data.frame(normalityPs))
normalityPsDfTran$segment <- names(normalityPsDf)


#####################Are our variances equal? NO
library(Rcmdr)
attach(sam)
equal<-leveneTest(sample$Count_,sample$TSEGNAME)
#to get p values out of levenes test list :
attributes(equal)
equaldf <- data.frame(equal)


#Order by means
mydata[order(mydata$B),]
write.csv(sample, file = "sample.csv")


#ANOVA
fit <- aov(Count_~TSEGNAME, data = sample)
summary(fit)
model.tables(fit)


#Tukey Test
tukey<-TukeyHSD(fit)
tukeydf<-data.frame(tukey[1])
plot(tukey)
write.csv(tukeydf, file = "TukeyResults.csv")

#Now for McDade's Probit/ and other regression models:
#. //Generate a numberic version of the tapestyry variable
#. //Generage the flag for being in a top-three tapestry
#. //generate a "customer flag" - a block group with at least one customer


#3.. probit customer toptap
#. //generate a "customer flag" - a block group with at least one customer
TAP_SPI$CustomerBin<- as.numeric(TAP_SPI$Count_ > 0)
#. //Generage the flag for being in a top-seven(mean) tapestry
TAP_SPI$Top7meanBin<- as.numeric(TAP_SPI$TSEGNAME == "Social Security Set"
| TAP_SPI$TSEGNAME == "College Towns"
| TAP_SPI$TSEGNAME == "Metro Renters"
| TAP_SPI$TSEGNAME == "Urban Chic"
| TAP_SPI$TSEGNAME == "Laptops and Lattes"
| TAP_SPI$TSEGNAME == "Trendsetters"
| TAP_SPI$TSEGNAME == "Emerald City")
#. //Generage the flag for being in a top-three(mean) tapestry
TAP_SPI$Top3meanBin<- as.numeric(TAP_SPI$TSEGNAME == "Social Security Set"
| TAP_SPI$TSEGNAME == "College Towns"
| TAP_SPI$TSEGNAME == "Metro Renters")
#. //Generage the flag for being in a top-three(mean) tapestry
TAP_SPI$Top3sumBin<- as.numeric(TAP_SPI$TSEGNAME == "Urban Chic" | TAP_SPI$TSEGNAME=="Emerald City" | TAP_SPI$TSEGNAME=="Laptops a
> nd Lattes")
                                

#probability that top three segments will contain a customer compared to not.
probit7 <- glm(TAP_SPI$CustomerBin ~ TAP_SPI$Top7TapBin, family= binomial(link = "probit"), 
                data = TAP_SPI)
probit3 <- glm(TAP_SPI$CustomerBin ~ TAP_SPI$Top3TapBin, family= binomial(link = "probit"), 
               data = TAP_SPI)
probit3sum <- glm(TAP_SPI$CustomerBin ~ TAP_SPI$Top3sumBin, family= binomial(link = "probit"), 
               data = TAP_SPI)

## model summary
summary(probit7)
summary(probit3)
summary(probit3sum)



#Then Maps

#Then Report








