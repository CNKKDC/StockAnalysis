# StockAnalysis



## 🔨 Tools

![](https://img.shields.io/badge/StockAnalysis-v1.0-brightgreen?style=flat-square) ![](https://img.shields.io/badge/Python-v3.8-blue?style=flat-square&logo=python&logoColor=white) ![](https://img.shields.io/pypi/v/PyMySQL?color=blue&label=PyMySQL&logo=python&logoColor=white&style=flat-square) ![](https://img.shields.io/pypi/v/xlwt?color=blue&label=xlwt&logo=python&logoColor=white&style=flat-square) ![](https://img.shields.io/pypi/v/xlrd?color=blue&label=xlrd&logo=python&logoColor=white&style=flat-square) ![](https://img.shields.io/pypi/v/beautifulsoup4?color=blue&label=bs4&logo=python&logoColor=white&style=flat-square) ![](https://img.shields.io/pypi/v/requests?color=blue&label=requests&logo=python&logoColor=white&style=flat-square)



![Twitter URL](https://img.shields.io/twitter/url?color=blue&label=Twitter&logo=twitter&logoColor=white&style=flat-square&url=https%3A%2F%2Ftwitter.com%2FMr_LiuYC) ![GitHub watchers](https://img.shields.io/github/watchers/LegendLiuYC/StockAnalysis?style=flat-square) ![GitHub forks](https://img.shields.io/github/forks/LegendLiuYC/StockAnalysis?style=flat-square)



##  🧷 Introduce

&emsp;&emsp;StockAnalysis is a program that analyzes stocks based on public funds, scoring stocks held by most funds in combination with their one-year interest rate and the percentage of positions held.Of course, if a fund's interest rate is high, then its holdings of stocks will be higher points;Conversely, if a fund has a negative one-year interest rate, it will have a corresponding deduction for the stocks it holds.So we know whether the stock is popular or not in the market.  
&emsp;&emsp;For the selection of the fund, this program will select the public offering open subscription stock and stock index fund when crawling data.  
&emsp;&emsp;Mainly for the Chinese stock market design. 




## 🎯 API

&emsp;&emsp;Information comes from [Eastmoney](https://fund.eastmoney.com)

```python
FUND_COMPANY_LIST_URL = "http://fund.eastmoney.com/company/default.html"
FUND_LIST_URL = "http://fund.eastmoney.com/Company/home/KFSFundNet?gsid={{companyId}}"
FUND_HOLD_URL = "http://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code={{fundId}}&topline={{DisplayTopItems}}&year=&month="
FUND_RATE_URL = "http://fund.eastmoney.com/pingzhongdata/{{fundId}}.js"
```



## ⌨️ Calculation

&emsp;&emsp;The starting fraction is `1`, and the multiple is `1`.First, check the one-year interest rate of the fund. If the interest rate is more than `100%`, then the multiple becomes `2`.If the interest rate is greater than `70%` and less than `100%`, then the multiple becomes `1.5`;If the interest rate is greater than `50%` and less than `70%`, then the multiple does not become `1`.If the interest rate is greater than `20%` and less than `50%`, the multiple becomes `0.2`;If the interest rate is negative, the multiple does not become `-1`.Then the first three stocks held by this fund are added, the value is `multiple * scores`.  
&emsp;&emsp;And so on until all the funds have been analysed.Finally, the stock data is sorted according to the number of points.



## 💡 About

&emsp;&emsp;Due to the short development cycle of this program, the research is not in-depth enough, so this program only provides a way of thinking for stock analysis.The data obtained by this program is not absolutely objective. The first data crawled is too little and the analysis is not comprehensive enough.Secondly, there is no more detailed scoring criteria for the fund's holding of stocks and the fund's longer interest rate;Finally, this program does not exclude environmental factors of the industry. For example, I knew before writing the program that "Kweichow Moutai" must be the first.  
&emsp;&emsp;I only put forward my ideas, interested friends can Fork my project or contact me, we discuss research together.

