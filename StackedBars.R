#samplegraphs

library(ggplot2)

df2 <- data.frame(supp=rep(c("VC", "OJ"), each=3),
                  dose=rep(c("D0.5", "D1", "D2"),2),
                  len=c(6.8, 15, 33, 4.2, 10, 29.5))
head(df2)



# Stacked barplot with multiple groups
blanktheme<-theme(panel.grid.major = element_blank(), panel.grid.minor = element_blank(),
               panel.background = element_blank(), axis.line = element_line(colour = "black"))

ggplot(data=df2, aes(x=dose, y=len, fill=supp)) +
  geom_bar(stat="identity",color="black")+ blanktheme





