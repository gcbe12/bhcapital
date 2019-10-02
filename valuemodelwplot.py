# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 18:24:23 2016

@author: gabri
"""

import numpy as np
import pandas as pd
import quandl
from matplotlib.finance import _quotes_historical_yahoo
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager


"""
data_xls = pd.read_excel('C:\\Users\\gabri\\Documents\\Courses\\Python for Finance\\RB1 Database\\RoburShortMeta.xlsx', 'ShortMeta', index_col=None)
data_xls.to_csv('C:\\Users\\gabri\\Documents\\Courses\\Python for Finance\\RB1 Database\\your_csv.csv', encoding='utf-8')
"""


#read company names
comp = pd.read_csv('C:\\Users\\gabri\\Documents\\Courses\\Python for Finance\\RB1 Database\\your_csv.csv')


quandl.ApiConfig.api_key = '81uUyGnzKYkF_SPoAC54'

#Income= quandl.get("RB1/0082_Income")


dataset_income = comp['Income'].tolist()
dataset_balance = comp['Balance'].tolist()
dataset_values = comp['Values'].tolist()
companyname = comp['Short Name'].tolist()
countryname = comp['Country'].tolist()
ticker = comp['YF Ticker'].tolist()

enddate=datetime.now()
begdate=enddate-relativedelta(years=2)
d=[]

"""
#x.iloc[3] to print the 4th row for example
#for datanum in dataset_list:
"""

plt.rc('axes', grid=True)
plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)

textsize = 9
left, width = 0.1, 0.8
rect1 = [left, 0.7, width, 0.2]
rect2 = [left, 0.3, width, 0.4]
rect3 = [left, 0.1, width, 0.2]


fig = plt.figure(facecolor='white')
axescolor = '#f6f6f6'  # the axes background color

ax1 = fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height
ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
ax2t = ax2.twinx()
ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)





for x in range(0, 10): 
    if countryname[x] == 'UK' or countryname[x] == 'USA':
        Income = quandl.get(dataset_income[x])   #gets the income data for company x
        Balance = quandl.get(dataset_balance[x]) #gets the balance data for company x
        Values = quandl.get(dataset_values[x]) #gets the values data for company x
        datelist = Income.index.tolist()  #list of dates for PE    
        if Income['EPS exc. extra'].iloc[-1] - Income['EPS exc. extra'].iloc[-2] > -5 and Income['Revenue'].iloc[-1] - Income['Revenue'].iloc[-2] > -5 and Values['Price:Earnings'].iloc[-1] < 50 and Values['Price:Book'].iloc[-1] < 20: 
            r = _quotes_historical_yahoo(ticker[x], begdate, enddate,asobject=True,adjusted=True)                
            G = pd.Series(r.aclose,r.date)  #start moving average
            g_mva = pd.rolling_mean(G,20)  #continue moving average                
            sdate = date(2016,1,4) #first day for moving average filter
            edate = date(2016,4,1) #last day for moving average filter
            tdate = date(2016,9,20)
            if g_mva.ix[edate]-g_mva.ix[sdate] > -50:
                d.append({'Company name':companyname[x],'cTicker':ticker[x],'Country':countryname[x],'Date end of last full period':datelist[-1],'PE at end of period':Values['Price:Earnings'].iloc[-1], 'P/B at end of period':Values['Price:Book'].iloc[-1],'z2015 vs 2014 EPS increase: ':Income['EPS exc. extra'].iloc[-1] - Income['EPS exc. extra'].iloc[-2],'Long term debt/Total Assets': Balance['Long Term Debt'].iloc[-1]/Balance['Total Assets'].iloc[-2],'v-3 month Moving average diff':g_mva.ix[edate]-g_mva.ix[sdate],'wBought at datae':edate,'xBought at moving Avg Price':g_mva.ix[edate],'wPresent datae':tdate,'xPresent Moving Avg Price':g_mva.ix[tdate]})
                prices = r.aclose
                #rsi = relative_strength(prices)
                fillcolor = 'darkgoldenrod'
                ax1.axhline(70, color=fillcolor)
                ax1.axhline(30, color=fillcolor)
                ax1.set_ylim(0, 100)
                ax1.set_yticks([30, 70])
                ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
                ax1.set_title('%s daily' % ticker)
                dx = r.aclose - r.close
                low = r.low + dx
                high = r.high + dx
                deltas = np.zeros_like(prices)
                deltas[1:] = np.diff(prices)
                up = deltas > 0
                ax2.vlines(r.date[up], low[up], high[up], color='black', label='_nolegend_')
                ax2.vlines(r.date[~up], low[~up], high[~up], color='black', label='_nolegend_')
                ma20 = moving_average(prices, 20, type='simple')
                ma200 = moving_average(prices, 200, type='simple')
                linema20, = ax2.plot(r.date, ma20, color='blue', lw=2, label='MA (20)')
                linema200, = ax2.plot(r.date, ma200, color='red', lw=2, label='MA (200)') 
                last = r[-1]
                s = '%s O:%1.2f H:%1.2f L:%1.2f C:%1.2f, V:%1.1fM Chg:%+1.2f' % (today.strftime('%d-%b-%Y'),
                last.open, last.high,
                last.low, last.close,
                last.volume*1e-6,
                last.close - last.open)
                t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)
                props = font_manager.FontProperties(size=10)
                leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
                leg.get_frame().set_alpha(0.5)
                plt.savefig('C:/Users/gabri/Documents/Courses/Python for Finance/figs/WB.pdf')
                plt.show()
        
df=pd.DataFrame(d)
writer = pd.ExcelWriter('C:/Users/gabri/Documents/Courses/Python for Finance/RB1 Database/analysisresults.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()



"""
#datelist = Valuesdate.index.tolist()

   Earnings per share, growth for last quarter:  filter negatives
   Revenue,  also growth:  filter negatives
   Long term debt/total assets:  debt ratio, want this value to be low
   Net income / sharehold equity:  should be 15-20%
   PE and PB
   
   
   print("Company: ",companyname[x])        
            print("2015 vs 2014 EPS increase: ", Income['EPS exc. extra'].iloc[-1] - Income['EPS exc. extra'].iloc[-2])
            print("2015 vs 2014 Revenue increase: ", Income['Revenue'].iloc[-1] - Income['Revenue'].iloc[-2])
            print("Long term debt/Total Assets:  ", Balance['Long Term Debt'].iloc[-1]/Balance['Total Assets'].iloc[-2])
            print("Date at bought:  ", datelist[-1],  "PE at bought:",  Valuesdate['Price:Earnings'].iloc[-1], "P/B at bought:  ", Valuesdate['Price:Book'].iloc[-1])
            print("Share Price at Bought:  ", Income['Share Price at EoP'].iloc[-1], "Share Price Today: ", Income['Last Share Price'].iloc[-1])


def relative_strength(prices, n=14):
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed >= 0].sum()/n  #all  gains
    down = -seed[seed < 0].sum()/n  #all losses
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1. + rs)

    for i in range(n, len(prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter

        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n - 1) + upval)/n
        down = (down*(n - 1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)

    return rsi  


            """       
