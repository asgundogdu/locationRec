
# construct eda-data.json
setwd('D:/Coursework/info viz')

library(tidyverse)
library(data.table)
library(geojsonio)

yfcc_usa <- fread(file = 'yfcc_usa.csv', showProgress=T)
sample <- sample_n(yfcc_usa, 100000) %>%
          arrange(date_taken)

sample$date <- paste(sample$month, sample$year, sep = ' ')

sample <- sample[sample$town!="",]
sample$url<-NULL
geojson_write(sample, lat = "latitude", lon = "longitude", file = "YFCC-USA-Town-Recommendation/data/eda-data.geojson")

# sample <- sp::SpatialPointsDataFrame(coords = sample[,c("longitude", "latitude")],
#                                    data = sample[,c(-3, -4)], 
#                                    proj4string = sp::CRS("+init=epsg:4326"))
# mapview::mapview(sample, zcol='state', pal='Set1')