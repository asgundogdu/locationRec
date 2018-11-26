
setwd('D:/Coursework/info viz')

library(tidyverse)
library(data.table)
library(lubridate)

# ------------------------------------------------------------------------------
#Boston 
# ------------------------------------------------------------------------------
# filter to Boston
# yfcc_usa <- fread(file = 'yfcc_usa_relevant_columns', showProgress=T)
# yfcc_boston <- yfcc_usa %>%
#   filter(str_detect(address, 'Boston'))
# rm(yfcc_usa)
# 
# extract regions
# yfcc_boston$poi  <- ifelse(str_detect(yfcc_boston$address, "POI"), gsub('\\+' , ' ', map(str_split(map(str_split(yfcc_boston$address, ','),1), ':'), 2)), NA)
# yfcc_boston$suburb  <- ifelse(str_detect(yfcc_boston$address, "Suburb"), gsub('\\+' , ' ', map(str_split(map(str_split(yfcc_boston$address, ','),2), ':'), 2)), NA)
# yfcc_boston$suburb[yfcc_boston$suburb=='Boston']<- NA

# seperate date/time
# yfcc_boston <- yfcc_boston %>%
#   separate(date_taken, into=c("date_taken", "time_taken"), sep=' ')

# merge autotags
# yfcc_autotags <- fread(file = 'yfcc100m_autotags', showProgress=T)
# yfcc_boston <- left_join(yfcc_boston, yfcc_autotags, by=c("pid"="V1"))
# names(yfcc_boston)[12] <- "autotags"
# rm(yfcc_autotags)
# fwrite(yfcc_boston , file = 'yfcc_usa_boston', showProgress=T, sep=',')

# convert date/time formats
# yfcc_boston$time_taken <- lubridate::hms(yfcc_boston$time_taken)
# yfcc_boston$date_taken <- lubridate::ymd(yfcc_boston$date_taken)
# save(yfcc_boston, file='yfcc_usa_boston.RData')
# write_csv(yfcc_boston, 'yfcc_usa_boston.csv')
# ------------------------------------------------------------------------------
# USA
# ------------------------------------------------------------------------------
# yfcc_usa <- fread(file = 'yfcc_usa_relevant_columns', showProgress=T)
# 
# # seperate date/time
# yfcc_usa <- yfcc_usa %>%
#   separate(date_taken, into=c("date_taken", "time_taken"), sep=' ')
# 
# yfcc_usa <- na.omit(yfcc_usa)
# 
# # extract regions
# # yfcc_usa$poi  <- ifelse(str_detect(yfcc_usa$address, "POI"), gsub('\\+',' ',map(str_split(lapply(str_split(gsub('(POI).*' , '\\1', yfcc_usa$address), ','), function(x) x[length(x)]),':'),2)), NA)
# # yfcc_usa$suburb  <- ifelse(str_detect(yfcc_usa$address, "Suburb"), gsub('\\+',' ',map(str_split(lapply(str_split(gsub('(Suburb).*' , '\\1', yfcc_usa$address), ','), function(x) x[length(x)]),':'),2)), NA)
# yfcc_usa$town  <- ifelse(str_detect(yfcc_usa$address, "Town"), gsub('\\+',' ',map(str_split(lapply(str_split(gsub('(Town).*' , '\\1', yfcc_usa$address), ','), function(x) x[length(x)]),':'),2)), NA)
# yfcc_usa$state  <- ifelse(str_detect(yfcc_usa$address, "State"), gsub('\\+',' ',map(str_split(lapply(str_split(gsub('(State).*' , '\\1', yfcc_usa$address), ','), function(x) x[length(x)]),':'),2)), NA)
# yfcc_usa$address <- NULL
# 
# # convert date/time formats
# yfcc_usa$date_taken <- lubridate::ymd(yfcc_usa$date_taken)
# yfcc_usa$time_taken <- NULL

# yfcc_usa <- yfcc_usa %>%
#   filter(state %in% state.name)

# yfcc_usa$year <- year(yfcc_usa$date_taken)
# yfcc_usa$month <- month.abb[month(yfcc_usa$date_taken)]

# yfcc_usa <- yfcc_usa %>%
#   filter(year>=2004, year<=2014) %>%
#   arrange(date_taken)

# fwrite(yfcc_usa, file='yfcc_usa.csv', sep=',', showProgress=T)

# yfcc_usa <- fread(file = 'yfcc_usa.csv', showProgress=T)

head(yfcc_usa)
library(mapview)
data <- sample_n(yfcc_usa, 100)

data <- sp::SpatialPointsDataFrame(coords = data[,c("longitude", "latitude")],
                       data = data[,c(-5, -6)], 
                       proj4string = sp::CRS("+init=epsg:28992"))

mapview(data, zcol='state', pal='Set1')


