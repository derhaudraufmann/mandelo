# this code is responsible for analyzing and visualizing both the crawled data from cnbc as well as
# the stock data from AlphaVantage

import matplotlib.pyplot as plt
import pymongo
from datetime import timedelta, date
from alpha_vantage.timeseries import TimeSeries
import changefinder
import plot


# obtain a free API key from https://www.alphavantage.co/ and insert it here, for querying stock data
alpha_vantage_API_Key = "PUT_YOUR_API_KEY_HERE"

granularity_string = 'day'
granularity = 1
symbol = "NVDA"
start_date = date(2018, 5, 14)
end_date = date(2018, 12, 28)

# stock price data
ts = TimeSeries(key=alpha_vantage_API_Key)
priceData = ts.get_daily(symbol, 'full')

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "kddm"

connection = pymongo.MongoClient(
    MONGODB_SERVER,
    MONGODB_PORT
)
db = connection[MONGODB_DB]
mentionCollection = db['mentions']


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


x = []
y = []
x_stockprice = []
y_stockprice = []
switcher = 0
accum_count = 0
accum_stockprice = 0.0
prev_stockprice = 0.0

cf = changefinder.ChangeFinder(r=0.25, order=2, smooth=7)
changeRet = []


for single_date in daterange(start_date, end_date):
    isodate = single_date.isoformat()
    mentionQuery = {"timestamp": isodate, "symbol": symbol}

    count = 0
    mentionInDb = mentionCollection.count_documents(mentionQuery)
    if mentionInDb == 1:
        mention = mentionCollection.find_one(mentionQuery)
        count = mention["count"]
    else:
        count = 0

    if isodate in priceData[0]:
        prev_stockprice = float(priceData[0][isodate]['4. close'])
    accum_stockprice = accum_stockprice + prev_stockprice

    accum_count = accum_count + count

    score = cf.update(accum_stockprice)
    changeRet.append(score)

    if switcher % granularity == 0:
        x.append(isodate)
        y.append(accum_count)
        accum_stockprice = accum_stockprice / granularity
        y_stockprice.append(accum_stockprice)
        x_stockprice.append((isodate))

        accum_stockprice = 0.0
        accum_count = 0

    switcher = switcher + 1

print(x)
print(y)

plot.plotPriceVSChange(x_stockprice, y_stockprice, changeRet)

ax = plt.subplot(111)
ax.bar(x, y, width=1)
ax.set_ylabel('Stock Mentions / ' + granularity_string)
ax.set_title(
    'Company name mentions per ' + granularity_string + ' against stock Price of ' + symbol + " from " + start_date.isoformat() + " to " + end_date.isoformat(),
    fontsize='18')

ax2 = ax.twinx()
ax2.plot(x_stockprice, y_stockprice, 'r')
ax2.tick_params('y', colors='r')
ax2.set_ylabel('Stockprice [USD]', color='r')

# changefinder
ax3 = ax.twinx()
ax3.plot(x_stockprice, changeRet, 'k')
ax3.tick_params('y', colors='k')
ax3.set_ylabel('Change [%]', color='k')


plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45, ha="left")
plt.gcf().set_size_inches(18.5, 10.5)
plt.gcf().savefig(symbol + '_' + granularity_string + 'ly.png', dpi=200)
plt.show()


# # changefinder plot
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(changeRet)
# ax2 = ax.twinx()
# ax2.plot(x_stockprice,'r')
# plt.show()
