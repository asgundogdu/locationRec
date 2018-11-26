
setwd('D:/Coursework/info viz')

library(tidyverse)
library(data.table)
library(geojsonio)

yfcc_usa <- fread(file = 'yfcc_usa.csv', showProgress=T)
sample <- sample_n(yfcc_usa, 10000) %>%
          arrange(date_taken)

sample$date <- paste(sample$month, sample$year, sep = ' ')

sample <- sample[sample$town!="",]

geojson_write(sample, lat = "latitude", lon = "longitude", file = "project/data/eda-data.geojson")

# sample <- sp::SpatialPointsDataFrame(coords = sample[,c("longitude", "latitude")],
#                                    data = sample[,c(-3, -4)], 
#                                    proj4string = sp::CRS("+init=epsg:4326"))
# mapview::mapview(sample, zcol='state', pal='Set1')

ht <- read_csv("ht-data.csv")

write(jsonlite::toJSON(ht), file = "project/data/ht-data.json")

sample$eval <- sample(c("F","T"), replace=TRUE, size=nrow(sample))

erdata <- toJSON(na.omit(sample %>%
  group_by(town, eval) %>%
  summarise(n=n()) %>%
  spread(eval, n) %>%
    arrange(desc(`T`)))[1:1000,])

write(erdata, file = "project/data/er-data.json")
