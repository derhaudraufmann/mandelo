import matplotlib.pyplot as plt

def plotPriceVSChange(xPrice, yPrice, change):
    ax = plt.subplot(111)
    ax.plot(xPrice, yPrice, 'r')
    ax.set_ylabel('Price [USD]')
    # ax.set_title(
    #     'Company name mentions per ' + granularity_string + ' against stock Price of ' + symbol + " from " + start_date.isoformat() + " to " + end_date.isoformat(),
    #     fontsize='18')
    # changefinder
    ax3 = ax.twinx()
    ax3.plot(xPrice, change, 'b')
    ax3.tick_params('y', colors='k')
    ax3.set_ylabel('Change [%]', color='k')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45, ha="left")
    plt.gcf().set_size_inches(18.5, 10.5)
    plt.gcf().savefig('test.png', dpi=200)
    plt.show()
#
# ax = plt.subplot(111)
# ax.bar(x, y, width=1)
# ax.set_ylabel('Stock Mentions / ' + granularity_string)
# ax.set_title(
#     'Company name mentions per ' + granularity_string + ' against stock Price of ' + symbol + " from " + start_date.isoformat() + " to " + end_date.isoformat(),
#     fontsize='18')
#
# ax2 = ax.twinx()
# ax2.plot(x_stockprice, y_stockprice, 'r')
# ax2.tick_params('y', colors='r')
# ax2.set_ylabel('Stockprice [USD]', color='r')
#
# # changefinder
# ax3 = ax.twinx()
# ax3.plot(x_stockprice, changeRet, 'k')
# ax3.tick_params('y', colors='k')
# ax3.set_ylabel('Change [%]', color='k')
#
#
# plt.setp(ax.xaxis.get_majorticklabels(), rotation=-45, ha="left")
# plt.gcf().set_size_inches(18.5, 10.5)
# plt.gcf().savefig(symbol + '_' + granularity_string + 'ly.png', dpi=200)
# plt.show()
#
#
# # # changefinder plot
# # fig = plt.figure()
# # ax = fig.add_subplot(111)
# # ax.plot(changeRet)
# # ax2 = ax.twinx()
# # ax2.plot(x_stockprice,'r')
# # plt.show()
