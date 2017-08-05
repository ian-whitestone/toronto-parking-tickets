setwd("/Users/whitesi/Documents/Programming/Python/toronto-parking/src/analysis")

source("Postgres.R")
library(ggplot2)
source("helper.R")
library(data.table)
library(dtplyr)
library(dplyr)
library(scales)
library(zoo)
library(RColorBrewer)
library(plyr)

number_ticks <- function(n) {function(limits) pretty(limits, n)}
##display.brewer.all() ##view all palettes with this
palette <- brewer.pal("YlGnBu", n=9)
###########################################
############  DATA LOADING ################
###########################################

conn = getPSconn('parking')

query = "
select extract(year from infraction_date) as yr, sum(fine_amt) as fines
from tickets
where infraction_code=15
and location2='393 UNIVERSITY AVE'
group by 1
;"
data = dbGetQuery(conn, query) %>% setDT
notify('data load complete')
#data = dbReadTable(conn, 'all_fsa_meta')


############################################
############  DATA CLEANING ################
############################################


#######################################
############  PLOTTING ################
#######################################
ggplot(data, aes(x=yr, y=fines, label=fines)) +
  geom_point() + geom_line() +  theme_dlin() +
  geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Sales', y='Median Sale Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = dollar,breaks=number_ticks(10))



merge = rbind(
  sold[region=='Toronto' & type == 'Detached', 
       .(med_price=as.integer(median(soldprice)), type='Sale', count=.N),
       by=.(yymm)],
  list[region=='Toronto' & type == 'Detached', 
       .(med_price=as.integer(median(askprice)), type='Listing', count=.N),
       by=.(yymm)]
)

## LISTING DATA IS SHIT BASED ON WHEN YOU STARTED SCRAPING!!
ggplot(merge[as.integer(substring(yymm,1,4))>2015,],
       aes(x=yymm, y=med_price, label=count, group=type, colour=type)) +
  geom_point() + geom_line() +  theme_dlin() +
  geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Sales', y='Median Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = dollar,breaks=number_ticks(10))





ggplot(sold[region=='Toronto' & type %in% homes & bdrm_grp %in% c('2','3','4'), 
            .(med_sale_price=as.integer(median(soldprice)), count=.N) ,by=.(yymm, bdrm_grp)],
       aes(x=yymm, y=med_sale_price, label=count, group=bdrm_grp, colour=bdrm_grp)) +
  geom_point() + geom_line() +  theme_dlin() +
  # geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  geom_label() +
  labs(title = 'Toronto Home Sales', y='Median Sale Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = dollar,breaks=number_ticks(10))


ggplot(sold[region=='Toronto' & type %in% c('Condo Apt'), 
            .(med_sale_price=as.integer(median(soldprice)), count=.N) ,by=.(yymm)],
       aes(x=yymm, y=med_sale_price, label=format.money(med_sale_price), group=1)) +
  geom_point() + geom_line() +  theme_dlin() +
  # geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  geom_label() +
  labs(title = 'Toronto Condo Sales', y='Median Sale Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = dollar,breaks=number_ticks(10))

ggplot(sold[region=='Toronto' & type %in% main_types, 
            .(med_sale_price=mean(soldprice), count=.N, dom = mean(dom)) ,by=.(yymm,type)],
       aes(x=yymm, y=dom, label=count, fill=type)) +
  geom_bar(stat='identity', position="dodge") +  theme_dlin() +
  # geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Sales', y='Average Days on the Market', x='Date', fill='Property Type') +
  scale_y_continuous(labels = comma, breaks=number_ticks(10))


ggplot(sold[region=='Toronto' & type %in% main_types, 
            .(med_sale_price=median(poa), count=.N) ,by=.(yymm,type)],
       aes(x=yymm, y=med_sale_price, label=count, fill=type)) +
  geom_bar(stat='identity', position="dodge") +  theme_dlin() +
  geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Sales - Price Over Ask', y='Median Price Over Ask', x='Date', fill='Property Type') +
  scale_y_continuous(labels = percent,breaks=number_ticks(10))


ggplot(list[region=='Toronto' & type %in% main_types & askprice<2e6 & inputdate>'2017-04-01', 
            .(med_list_price=as.integer(median(askprice)), count=.N) ,by=.(yymm,type)],
       aes(x=yymm, y=med_list_price, label=count, fill=type)) +
  geom_bar(stat='identity', position="dodge") +  theme_dlin() +
  geom_text(position=position_dodge(width= 0.9), vjust=-0.25) +
  labs(title = 'Toronto Property Listings', y='Median Asking Price', x='Date', fill='Property Type') +
  scale_y_continuous(labels = comma,breaks=number_ticks(10))


##PLOTTING TO DO:

##SOLD


##LIST
# track number of price changes