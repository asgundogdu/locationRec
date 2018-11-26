
setwd('D:/Coursework/info viz')

library(tidyverse)
library(photon)

yfcc_boston <- read_csv('yfcc_usa_boston.csv')

data <- yfcc_boston[is.na(yfcc_boston$poi),c(1,7,8)]

data <- split(data, rep(1:10))
lapply(data, function(x) {
  temp<-reverse(x$longitude, x$latitude)
  write_csv(temp, format(Sys.time(), "%H%M%S"))
})

