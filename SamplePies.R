df <- data.frame(
  group = c("Male", "Female", "Child"),
  value = c(25, 25, 50)
)
head(df)

library(ggplot2)
# Barplot
bp<- ggplot(df, aes(x="", y=value, fill=group))+
  geom_bar(width = 1, stat = "identity")
bp

pie <- bp + coord_polar("y", start=0)
pie

pie + scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9"))

# use brewer color palettes
pie + scale_fill_brewer(palette="Dark2")