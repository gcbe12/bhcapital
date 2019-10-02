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
from matplotlib.backends.backend_pdf import PdfPages


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

#datetime documentation: https://docs.python.org/3/library/datetime.html
enddate=datetime.now()
begdate=enddate-relativedelta(years=2)
d=[]


#x.iloc[3] to print the 4th row for example
#for datanum in dataset_list:

#len(countryname)

for x in range(0, 10): 
    if countryname[x] == 'UK' or countryname[x] == 'USA':
        Income = quandl.get(dataset_income[x])   #gets the income data for company x
        Balance = quandl.get(dataset_balance[x]) #gets the balance data for company x
        Values = quandl.get(dataset_values[x]) #gets the values data for company x
        datelist = Income.index.tolist()  #list of dates for PE    
        try:   
            if Income['EPS exc. extra'].iloc[-1] - Income['EPS exc. extra'].iloc[-2] > 0 and Income['Revenue'].iloc[-1] - Income['Revenue'].iloc[-2] > 0 and Values['Price:Earnings'].iloc[-1] < 15 and Values['Price:Book'].iloc[-1] < 5: 
                p = _quotes_historical_yahoo(ticker[x], begdate, enddate,asobject=True,adjusted=True)                
                G = pd.Series(p.aclose,p.date)  #start moving average
                g_mva = pd.rolling_mean(G,50)  #continue moving average                
                sdate = date(2016,1,4) #first day for moving average filter
                edate = date(2016,4,1) #last day for moving average filter
                tdate = date(2016,9,20)
                if g_mva.ix[edate]-g_mva.ix[sdate] > 0:
                    d.append({'Company name':companyname[x],'cTicker':ticker[x],'Country':countryname[x],'Date end of last full period':datelist[-1],'PE at end of period':Values['Price:Earnings'].iloc[-1], 'P/B at end of period':Values['Price:Book'].iloc[-1],'z2015 vs 2014 EPS increase: ':Income['EPS exc. extra'].iloc[-1] - Income['EPS exc. extra'].iloc[-2],'Long term debt/Total Assets': Balance['Long Term Debt'].iloc[-1]/Balance['Total Assets'].iloc[-2],'v-3 month Moving average diff':g_mva.ix[edate]-g_mva.ix[sdate],'wBought at datae':edate,'xBought at moving Avg Price':g_mva.ix[edate],'wPresent datae':tdate,'xPresent Moving Avg Price':g_mva.ix[tdate]})
                    with PdfPages('C:/Users/gabri/Documents/BHCapital/analysis/analysis '+str(companyname[x])+'.pdf') as pdf:
                        plt.figure(figsize=(8, 8))  
                        plt.plot(p.date,p.aclose)
                        plt.plot(p.date,g_mva)
                        plt.xlabel('Year')
                        plt.ylabel('close price and 50 day moving average')
                        plt.title(companyname[x] + '   Ticker:' + ticker[x])    
                        pdf.savefig()  # saves the current figure into a pdf page
                        plt.close()
 
                        plt.figure(figsize=(10, 10))
                        plt.plot(Values['Price:Earnings'])
                        plt.plot(Values['Price:Book'])
                        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=1,ncol=2, borderaxespad=0.)
                        plt.title(companyname[x] + ':   PE and PB ratios')
                        pdf.savefig()  # saves the current figure into a pdf page
                        plt.close()
                        
                        plt.figure(figsize=(8, 8))  
                        plt.plot(Balance['Long Term Debt']/Balance['Total Assets'])
                        plt.title(companyname[x] + ':   Long Term Debt / Total Assets')    
                        pdf.savefig()  # saves the current figure into a pdf page
                        plt.close()
                        
                        plt.figure(figsize=(8, 8))  
                        plt.plot(Income['EPS exc. extra'])
                        plt.title(companyname[x] + ':   Earnings per Share excluding extra')    
                        pdf.savefig()  # saves the current figure into a pdf page
                        plt.close()
                        
                        plt.figure(figsize=(8, 8))  
                        plt.plot(Income['Revenue'])
                        plt.title(companyname[x] + ':  Revenue')    
                        pdf.savefig()  # saves the current figure into a pdf page
                        plt.close()
        except:
                print ("No data for: ", companyname[x], "   ",dataset_income[x])
   
df=pd.DataFrame(d)
writer = pd.ExcelWriter('C:/Users/gabri/Documents/BHCapital/analysisresults.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1')
writer.save()


#datelist = Valuesdate.index.tolist()
"""
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
