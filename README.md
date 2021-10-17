# Financial Modeling Prep API
 A python wrapper for Financial Modeling Prep API.
 
This wrapper follows API documentation on the following link:
https://financialmodelingprep.com/developer/docs

Each subchapter is covered by its own subclass. There are some exceptions,
mostly for things that are duplicated and are already similary presented
in other chapters.

For easier navigation, all of the classes, subclasses and definitions are shown below.

```
class FMP:
    def request(self, url: str):
    class StockFundamentals:
        def getFinancialStatementList(self):
        def getCompanyFinancialStatement(self, ticker: str, statement_type: str, period: str, limit: int = None):
        def getCompanyFinancialStatementAsReported(self, ticker: str, statement_type: str, period: str, limit: int = None):
        def getListOfDatesAndLinks(self, ticker: str):
        def getReportsOnForm10K(self, ticker: str, year: str, period: str):
        def getSharesFloat(self, ticker: str):
    class StockFundamentalsAnalysis:
        def getCompanyFinancialRatios(self, ticker: str, period: str = None, limit: int = None):
        def getCompanyEnterpriseValue(self, ticker: str, period: str, limit: int = None):
        def getFinancialStatementsGrowth(self, ticker: str, statement_type: str, limit: int = None):
        def getCompanyKeyMetrics(self, ticker: str, period: str = None, limit: int = None):
        def getCompanyFinancialGrowth(self, ticker: str, period: str, limit: int = None):
        def getCompanyRating(self, ticker: str):
        def getCompanyHistoricalRating(self, ticker: str, limit: int):
        def getCompanyDiscountedCashflow(self, ticker: str):
        def getCompanyHistoricalDiscountedCashflow(self, ticker: str, period: str = None, limit: int = None):
    class StockCalendars:
        def getEarningsCalendar(self, from_: str = None, to_: str = None):
        def getHistoricalEarningsCalendar(self, ticker: str, limit: int):
        def getIPOCalendar(self, from_: str = None, to_: str = None):
        def getStockSplitCalendar(self, from_: str = None, to_: str = None):
        def getDividendCalendar(self, from_: str = None, to_: str = None):
        def getEconomicCalendar(self, from_: str = None, to_: str = None):
    class StockLookUpTool:
        def getSearch(self, query: str, exchange: str = None, limit: int = None):
        def getTickerSearch(self, query: str, exchange: str = None, limit: int = None):
    class CompanyInformation:
        def getCompanyProfile(self, ticker: str):
        def getKeyExecutives(self, ticker: str):
        def getMarketCapitalization(self, ticker: str):
        def getHistoricalMarketCapitalization(self, ticker: str, limit: int = None):
        def getCompanyOutlook(self, ticker: str):
        def getStockPeers(self, ticker: str):
        def getNYSETradingHours(self):
        def getDelistedCompanies(self, limit: int = None):
    class StockNews:
        def getFMPArticles(self, page: int, size: int):
        def getStockNews(self, tickers: str = None, limit: int = None):
        def getPressRelease(self, ticker: str, limit: int = None):
    class MarketPerformace:
        def getSectorsPERatio(self, date: str = None, exchange: str = None):
        def getIndustriesPERatio(self, date: str = None, exchange: str = None):
        def getStockMarketSectorPerformance(self):
        def getHistoricalStockMarketSectorPerformance(self, limit: int = None):
        def getMostGainerStock(self):
        def getMostLoserStock(self):
        def getMostActiveStock(self):
    class AdvancedData:
        def getCotTradingSymbolsList(self):
        def getCommitmentsOfTradersReport(self, ticker: str = None, from_: str = None, to_: str = None):
        def getCommitmentsOfTradersAnalysis(self, ticker: str = None, from_: str = None, to_: str = None):
    class StockStatistics:
        def getSocialSentiment(self, ticker: str, limit: int = None):
        def getStockGrade(self, ticker: str, limit: int = None):
        def getEarningsSurprises(self, ticker: str):
        def getAnalystEstimates(self, ticker: str, period: str = None, limit: int = None):
    class InsiderTrading:
        def getStockInsiderTrading(self, ticker: str = None, companyCik: str = None, reportingCik: str = None, limit: int = None):
        def getCikMapper(self):
        def getInsiderTradingRSSFeed(self, limit: int = None):
        def getFailToDeliver(self, ticker: str):
    class Prices:
        def getQuote(self, tickers: str):
        def getRealTimePrice(self, ticker: str):
        def getPriceList(self, exchange: str):
        def getHistoricalPrices(self, ticker: str, timeframe: str):
        def getHistoricalDividends(self, ticker: str):
        def getHistoricalStockSplits(self, ticker: str):
        def getSurvivorshipBiasFreeEod(self, ticker: str, date: str):
        def getDailyIndicators(self, ticker: str, period: int, type: str):
        def getIntradayIndicators(self, ticker: str, timeframe: str, period: int, type: str):
    class FundHoldings:
        def getEtfHolders(self, ticker: str):
        def getInstitutionalHolders(self, ticker: str):
        def getMutualFundHolders(self, ticker: str):
        def getEtfSectorWeightings(self, ticker: str):
        def getEtfCountryWeightings(self, ticker: str):
        def get13FList(self):
        def getCikByCompanyName(self, companyName: str):
        def getCompanyNameByCik(self, cik: str):
        def getForm13fByCik(self, cik: str, date: str):
        def getFilingDatesByCik(self, cik: str):
        def getCusipMapper(self, cusip: str):
    class StockList:
        def getSymbolsList(self):
        def getTradableSymbolsList(self):
        def getEtfList(self):
    class BulkAndBatch:
    class MarketIndexes:
        def getHistoricalSandP500ConstituentsList(self):
        def getListOfNasdaq100Companies(self):
        def getListOfDowJonesCompanies(self):
        def getHistoricalDowJonesConstituentsList(self):
        def getSymbolList(self, ticker_type: str):
        
```

You can use this wrapper in the following fashion:
```
from FMP_api import FMP

API_KEY = 'YOUR API KEY'

fmp = FMP(API_KEY)

fmp.StockFundamentals.getFinancialStatementList()
fmp.StockFundamentals.getCompanyFinancialStatement('AAPL', 'income-statement', 'annual',100)
fmp.StockFundamentals.getCompanyFinancialStatementAsReported('AAPL', 'income-statement', 'annual',100)
fmp.StockFundamentals.getListOfDatesAndLinks('AAPL')

fmp.StockFundamentalsAnalysis.getCompanyFinancialRatios('AAPL', 'annual', 100)
fmp.StockFundamentalsAnalysis.getCompanyEnterpriseValue('AAPL', 'annual', 100)

...
```
