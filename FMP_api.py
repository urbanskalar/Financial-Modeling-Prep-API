"""
FMP_api.py: A python wrapper for Financial Modeling Prep API.

This wrapper follows API documentation on the following link:
https://financialmodelingprep.com/developer/docs

Each subchapter is covered by its own subclass. There are some exceptions,
mostly for things that are duplicated and are already similary presented in
in other chapters.
"""

__author__ = 'Urban Skalar'
__license__ = 'GNU General Public License v3.0'


import requests
import datetime


class FMP:
    """
    Wrapper for Financial Modeling Prep API.

    https://financialmodelingprep.com/developer/docs
    """

    def __init__(self, api_key: str):
        """
        Constructs the FMP instance.
        """

        self.API_KEY = api_key

        # Start new session
        self.session = requests.Session()

        # Construct objects from children classes
        self.StockFundamentals = self.StockFundamentals(self)
        self.StockFundamentalsAnalysis = self.StockFundamentalsAnalysis(self)
        self.StockCalendars = self.StockCalendars(self)
        self.StockLookUpTool = self.StockLookUpTool(self)
        self.CompanyInformation = self.CompanyInformation(self)
        self.StockNews = self.StockNews(self)
        self.MarketPerformance = self.MarketPerformace(self)
        self.AdvancedData = self.AdvancedData(self)
        self.StockStatistics = self.StockStatistics(self)
        self.InsiderTrading = self.InsiderTrading(self)
        self.Prices = self.Prices(self)
        self.FundHoldings = self.FundHoldings(self)
        self.StockList = self.StockList(self)
        self.BulkAndBatch = self.BulkAndBatch(self)
        self.MarketIndexes = self.MarketIndexes(self)

    def request(self, url: str):

        # Send request and save response
        resp = self.session.get(url)

        # Check if response code is 200
        if resp.status_code == 200:
            return resp.json()
        else:
            raise Exception(
                'Expected response "200 - OK", instead you got "' + str(resp.status_code) + ' - ' + str(
                    resp.content) + '"')

    class StockFundamentals:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getFinancialStatementList(self):
            """
            Financial Statements List:

            https://financialmodelingprep.com/developer/docs/financial-statements-list

            This endpoint allows you to get a list of all companies for which the API has financial statements.
            We cover the New York Stock Exchange (NYSE), the New York Stock Exchange (NASDAQ), international exchanges,
            and more. Because we're growing all the time, this list will be updated on a regular basis.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={YOUR_API_KEY}'.format(
                YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCompanyFinancialStatement(self, ticker: str, statement_type: str, period: str, limit: int = None):
            """
            Company Financial Statements:

            https://financialmodelingprep.com/developer/docs/financial-statement-free-api

            This endpoint returns company financial statements. SEC forms 10-K, 10-Q, and 8-K are used to obtain all
            financial statements for US companies. We offer data in JSON and CSV formats. We use values from statements
            for a variety of purposes, including growth endpoint, ratios endpoint, and more. Check out our page on how
            we parse statements for more information.

            Parameter           data type           example
            ticker              str                 'AAPL'
            statement_type      str                 'income-statement'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if statement_type not in ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']:
                raise ValueError('Parameter "statement_type" not specified correctly. Should be "income-statement", '
                                 '"balance-sheet-statement" or "cash-flow-statement"!')
            if period not in ['annual', 'quarter']:
                raise ValueError('Parameter "period" not specified correctly. Should be "annual" or "quarter"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/{STATEMENT_TYPE}/{TICKER}?period={PERIOD}&apikey=' \
                  '{YOUR_API_KEY}'.format(STATEMENT_TYPE=statement_type, TICKER=ticker, PERIOD=period,
                                          YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if C
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getCompanyFinancialStatementAsReported(self, ticker: str, statement_type: str, period: str, limit: int = None):
            """
            Company Financial Statements As Reported:

            https://financialmodelingprep.com/developer/docs/financial-statement-as-reported

            This endpoint returns reported financial values from company statements. It can be used to get values that
            our financial statements endpoint doesn't have. The number of fields and their names differ because they are
            determined by the tag from the company's statements and the amount of information they provide.

            Parameter           data type           example
            ticker              str                 'AAPL'
            statement_type      str                 'income-statement'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if statement_type not in ['income-statement', 'balance-sheet-statement', 'cash-flow-statement',
                                      'financial-statement-full']:
                raise ValueError('Parameter "statement_type" not specified correctly. Should be "income-statement", '
                                 '"balance-sheet-statement", "cash-flow-statement" or "financial-statement-full"!')
            if period not in ['annual', 'quarter']:
                raise ValueError('Parameter "period" not specified correctly. Should be "annual" or "quarter"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/{STATEMENT_TYPE}-as-reported/{TICKER}?period=' \
                  '{PERIOD}&apikey={YOUR_API_KEY}'.format(STATEMENT_TYPE=statement_type, TICKER=ticker, PERIOD=period,
                                                          YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getListOfDatesAndLinks(self, ticker: str):
            """
            List of dates and links:

            https://financialmodelingprep.com/developer/docs/list-dates-links

            The endpoint returns all statements from the company that include links to the JSON and XLSX versions of the
            statement. You won't need to know the year or period for the xlsx and json versions of statements because
            this endpoint will automatically return the appropriate link.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/financial-reports-dates?symbol={TICKER}&apikey=' \
                  '{YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getReportsOnForm10K(self, ticker: str, year: str, period: str):
            """
            Annual Reports on Form 10-K:

            https://financialmodelingprep.com/developer/docs/annual-report-form

            Financial Data access Quarterly Earnings Reports and Annual Reports on Form 10-K. The 10-K report is
            equivalent to the annual report that a company publish, the 10-Q is for the quarterly report. Each company
            has a different fiscal year, for example AAPL end its fiscal year in september. This endpoint uses the
            calendar year.

            Parameter           data type           example
            ticker              str                 'AAPL'
            year                str                 '2020'
            period              str                 'Q1'
            """

            # Check input parameters
            if period not in ['FY', 'Q1', 'Q2', 'Q3', 'Q4']:
                raise ValueError('Parameter "period" not specified correctly. Should "FY", "Q1", "Q2", "Q3" or "Q4"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/financial-reports-json?symbol={TICKER}&year=' \
                  '{YEAR}&period={PERIOD}&apikey={YOUR_API_KEY}'.format(YEAR=year, TICKER=ticker, PERIOD=period,
                                                                        YOUR_API_KEY=self.parent.API_KEY)
            return self.parent.request(url)

        def getSharesFloat(self, ticker: str):
            """
            Shares Float:

            https://financialmodelingprep.com/developer/docs/shares-float

            The number of shares available for trading is known as the float. The more floatable shares there are, the
            better. RSUs and remaining shares are used to calculate float shares.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/shares_float?symbol={TICKER}&apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

    class StockFundamentalsAnalysis:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getCompanyFinancialRatios(self, ticker: str, period: str = None, limit: int = None):
            """
            Company Financial Ratios:

            https://financialmodelingprep.com/developer/docs/financial-ratio-free-api

            This endpoint returns financial ratios for companies to help in company analysis. This endpoint computes
            ratios for each financial statement presented by the company (you can find those on our financial statements
            endpoint). This endpoint supports all of our API's companies. Visit our formula page to learn more about
            how we calculate those ratios.

            Parameter           data type           example
            ticker              str                 'AAPL'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if period not in ['annual', 'quarter', None]:
                raise ValueError('Parameter "period" not specified correctly. Should be "annual", "quarter" or None'
                                 ' for TTM!')

            # Generate url
            if period:
                url = 'https://financialmodelingprep.com/api/v3/ratios/{TICKER}?period={PERIOD}&apikey={YOUR_API_KEY}'.format(
                    TICKER=ticker, PERIOD=period, LIMIT=limit, YOUR_API_KEY=self.parent.API_KEY)
                # Append limit to url if available
                if limit:
                    url = url + '&limit={LIMIT}'.format(LIMIT=limit)
            else:
                url = 'https://financialmodelingprep.com/api/v3/ratios-ttm/{TICKER}?apikey={YOUR_API_KEY}'.format(
                    TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCompanyEnterpriseValue(self, ticker: str, period: str, limit: int = None):
            """
            Company Enterprise Value:

            https://financialmodelingprep.com/developer/docs/company-enterprise-value-api

            Get a company enterprise value based on its financial statement, it is calculated from Market Value.
            The enterprise Value is a proportion of an organization's absolute worth, frequently utilized as a more
            thorough option in contrast to value market capitalization.
            Its estimation the market capitalization of an organization yet in addition present moment and long
            obligation just as any money on the organization's asset report.

            Parameter           data type           example
            ticker              str                 'AAPL'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if period not in ['annual', 'quarter']:
                raise ValueError('Parameter "period" not specified correctly. Should be "annual" or "quarter"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/enterprise-values/{TICKER}?period={PERIOD}&apikey=' \
                  '{YOUR_API_KEY}'.format(TICKER=ticker, PERIOD=period, YOUR_API_KEY=self.parent.API_KEY)
            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getFinancialStatementsGrowth(self, ticker: str, statement_type: str, limit: int = None):
            """
            Financial Statements Growth:

            https://financialmodelingprep.com/developer/docs/financial-statements-growth

            This endpoint allows you to examine how the company has grown since its initial public offering. It provides
            details such as revenue growth and net income growth. Our financial statements endpoint is used to calculate
            all fields. Every company with statements is supported by Growth Endpoint. You can look up those stocks
            using the financial statements list endpoint.

            Parameter           data type           example
            ticker              str                 'AAPL'
            statement_type      str                 'income-statement'
            limit               int                 20
            """

            # Check input parameters
            if statement_type not in ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']:
                raise ValueError('Parameter "statement_type" not specified correctly. Should be "income-statement", '
                                 '"balance-sheet-statement" or "cash-flow-statement"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/{STATEMENT_TYPE}-growth/{TICKER}?apikey={YOUR_API_KEY}'.format(
                STATEMENT_TYPE=statement_type, TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getCompanyKeyMetrics(self, ticker: str, period: str = None, limit: int = None):
            """
            Company Key Metrics:

            https://financialmodelingprep.com/developer/docs/company-key-metrics-api

            Get Company Key Metrics such as Market capitalization, PE ratio, Price to Sales Ratio, POCF ratio, Graham
            Net-Net.
            The key metrics are calculated quarter by quarter, year by year. The change in company metrics is essential
            for valuating a company. You can also access the metrics TTM.

            Parameter           data type           example
            ticker              str                 'AAPL'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if period not in ['annual', 'quarter', None]:
                raise ValueError('Parameter "period" not specified correctly. Should be "annual", "quarter" or None'
                                 ' for TTM!')
            if not period and not limit:
                raise ValueError('When trying to get TTM data, you must specify only "ticker" and'
                                 '"limit" parameters, otherwise API will not return data!')

            # Generate url
            if period:
                url = 'https://financialmodelingprep.com/api/v3/key-metrics/{TICKER}?period={PERIOD}&apikey=' \
                      '{YOUR_API_KEY}'.format(TICKER=ticker, PERIOD=period, YOUR_API_KEY=self.parent.API_KEY)
                # Append limit to url if available
                if limit:
                    url = url + '&limit={LIMIT}'.format(LIMIT=limit)
            else:
                url = 'https://financialmodelingprep.com/api/v3/key-metrics-ttm/{TICKER}?limit={LIMIT}&apikey=' \
                      '{YOUR_API_KEY}'.format(TICKER=ticker, LIMIT=limit, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCompanyFinancialGrowth(self, ticker: str, period: str, limit: int = None):
            """
            Company Financial Growth:

            https://financialmodelingprep.com/developer/docs/company-financial-statement-growth-api

            Get the Financial Statement Growth of a company based on its financial statement, it compares previous
            financial statement to get growth of all its statement.
            The growth is calculated quarter by quarter, year by year. The change in company metrics is essential for
            valuating a company.

            Parameter           data type           example
            ticker              str                 'AAPL'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if period not in ['annual', 'quarter']:
                raise ValueError('Parameter "period" not specified correctly. Should be "annual" or "quarter"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/financial-growth/{TICKER}?period={PERIOD}&apikey=' \
                  '{YOUR_API_KEY}'.format(TICKER=ticker, PERIOD=period, YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getCompanyRating(self, ticker: str):
            """
            Company Rating:

            https://financialmodelingprep.com/developer/docs/companies-rating-free-api

            Get the rating of a company based on its financial statement, Discounted cash flow analysis, financial
            rations and its intrinsic value.
            Our ratings are based on companies being able to cover their debts and the strength of their ratios.
            If you need more details on our formula used to calculate our financial ratios to have a full spectrum
            of a each of the component of our ratings.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/rating/{TICKER}?apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCompanyHistoricalRating(self, ticker: str, limit: int):
            """
            Company Historical Rating:

            https://financialmodelingprep.com/developer/docs/companies-rating-free-api

            Get the rating of a company based on its financial statement, Discounted cash flow analysis, financial
            rations and its intrinsic value.
            Our ratings are based on companies being able to cover their debts and the strength of their ratios.
            If you need more details on our formula used to calculate our financial ratios to have a full spectrum
            of a each of the component of our ratings.

            Parameter           data type           example
            ticker              str                 'AAPL'
            limit               int                 20
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical-rating/{TICKER}?limit={LIMIT}&apikey=' \
                  '{YOUR_API_KEY}'.format(TICKER=ticker, LIMIT=limit, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCompanyDiscountedCashflow(self, ticker: str):
            """
            Company Discounted cash flow value:

            https://financialmodelingprep.com/developer/docs/companies-dcf-reports-free-api

            Access a stock discounted cash flow value. This value represents a stock intrinsic value calculated from its
            free cash flow analysis. If this value is over the current stock price the stock is considered undervalued
            and vice versa.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/discounted-cash-flow/{TICKER}?apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCompanyHistoricalDiscountedCashflow(self, ticker: str, period: str = None, limit: int = None):
            """
            Company Historical Discounted cash flow value:

            https://financialmodelingprep.com/developer/docs/companies-dcf-reports-free-api

            Access a stock discounted cash flow value. This value represents a stock intrinsic value calculated from its
            free cash flow analysis. If this value is over the current stock price the stock is considered undervalued
            and vice versa.

            Parameter           data type           example
            ticker              str                 'AAPL'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if period and limit:
                raise ValueError('You can only use either "period" or "limit" parameter, not both at once!')
            elif period:
                if period not in ['annual', 'quarter']:
                    raise ValueError('Parameter "period" not specified correctly. Should be "annual" or "quarter"!')

            # Generate url
            if period:
                url = 'https://financialmodelingprep.com/api/v3/historical-discounted-cash-flow-statement/' \
                      '{TICKER}?period={PERIOD}&apikey={YOUR_API_KEY}'.format(TICKER=ticker, PERIOD=period,
                                                                              YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v3/historical-daily-discounted-cash-flow/' \
                      '{TICKER}?limit={LIMIT}&apikey={YOUR_API_KEY}'.format(TICKER=ticker, LIMIT=limit,
                                                                            YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

    class StockCalendars:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getEarningsCalendar(self, from_: str = None, to_: str = None):
            """
            Earnings Calendar:

            https://financialmodelingprep.com/developer/docs/earnings-calendar-api

            Access Earnings calendar to Access all Earnings Calendar date such as AAPL, FB , MSFT next earnings date,
            EPS and EPS estimated.
            You will be able to Track companies who release earnings reports ordered by date.

            Parameter           data type           example
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            if from_ and to_:
                url = 'https://financialmodelingprep.com/api/v3/earning_calendar?from={FROM}&to={TO}&apikey=' \
                      '{YOUR_API_KEY}'.format(FROM=from_, TO=to_, YOUR_API_KEY=self.parent.API_KEY)
            elif from_:
                url = 'https://financialmodelingprep.com/api/v3/earning_calendar?from={FROM}&apikey={YOUR_API_KEY}'.format(
                    FROM=from_, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v3/earning_calendar'

            return self.parent.request(url)

        def getHistoricalEarningsCalendar(self, ticker: str, limit: int):
            """
            Earnings Calendar:

            https://financialmodelingprep.com/developer/docs/earnings-calendar-api

            Access Earnings calendar to Access all Earnings Calendar date such as AAPL, FB , MSFT next earnings date,
            EPS and EPS estimated.
            You will be able to Track companies who release earnings reports ordered by date.

            Parameter           data type           example
            ticker              str                 'AAPL'
            limit               int                 20
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical/earning_calendar/{TICKER}?limit=' \
                  '{LIMIT}&apikey={YOUR_API_KEY}'.format(TICKER=ticker, LIMIT=limit, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getIPOCalendar(self, from_: str = None, to_: str = None):
            """
            IPO Calendar:

            https://financialmodelingprep.com/developer/docs/ipo-calendar

            We support a few calendars, and IPO Calendar is one of them. This calendar keeps track of all IPOs currently
            taking place in the market. Action shares exchange price range and other fields are among the fields
            returned. You can use it to keep track of what interesting stocks are going public and when they are going
            public. You can specify a date range, and if you don't  you will get the most recent IPOs. All IPOs are
            added within a few days of their launch, you can get those at our profile endpoint.

            Parameter           data type           example
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            if from_ and to_:
                url = 'https://financialmodelingprep.com/api/v3/ipo_calendar?from={FROM}&to={TO}&apikey={YOUR_API_KEY}'.format(
                    FROM=from_, TO=to_, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v3/ipo_calendar?from={FROM}&apikey={YOUR_API_KEY}'.format(
                    FROM=from_, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getStockSplitCalendar(self, from_: str = None, to_: str = None):
            """
            Stock Split Calendar:

            https://financialmodelingprep.com/developer/docs/stock-split-calendar

            Access a stock split calendar that includes the numerator, denominator, and exact date of the split. Stock
            splits are a way for publicly traded companies to improve stock liquidity, typically, companies increase the
            number of shares outstanding, which lowers the stock price, however, the number of shares outstanding can
            also be reduced, increasing the stock price. The value of a company does not change as a result of a stock
            split.

            Parameter           data type           example
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            if from_ and to_:
                url = 'https://financialmodelingprep.com/api/v3/stock_split_calendar?from={FROM}&to={TO}&apikey=' \
                      '{YOUR_API_KEY}'.format(FROM=from_, TO=to_, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v3/stock_split_calendar?from={FROM}&apikey={YOUR_API_KEY}'.format(
                    FROM=from_, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getDividendCalendar(self, from_: str = None, to_: str = None):
            """
            Dividend Calendar:

            https://financialmodelingprep.com/developer/docs/dividend-calendar

            Access Dividend calendar to get dividends within period of time.
            Profit stocks appropriate a part of the organization's income to financial backers consistently.
            In addition to Stock paying dividend, Stock Market Index plays an important role in the flow of money within
            the stock market.

            Parameter           data type           example
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            if from_ and to_:
                url = 'https://financialmodelingprep.com/api/v3/stock_dividend_calendar?from={FROM}&to={TO}&apikey=' \
                      '{YOUR_API_KEY}'.format(FROM=from_, TO=to_, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v3/stock_dividend_calendar?from={FROM}&apikey=' \
                      '{YOUR_API_KEY}'.format(FROM=from_, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getEconomicCalendar(self, from_: str = None, to_: str = None):
            """
            Economic Calendar:

            https://financialmodelingprep.com/developer/docs/economic-calendar

            This is an economic calendar that returns all of the world's major economic events and numbers. It has a
            significant impact on currency and stock market prices. It returns fields such as the name of the event, the
            country, the previous and current value of the event, and more. Every 15 minutes, the calendar is updated.

            Parameter           data type           example
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            if from_ and to_:
                url = 'https://financialmodelingprep.com/api/v3/economic_calendar?from={FROM}&to={TO}&apikey=' \
                      '{YOUR_API_KEY}'.format(FROM=from_, TO=to_, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v3/economic_calendar?from={FROM}&apikey={YOUR_API_KEY}'.format(
                    FROM=from_, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

    class StockLookUpTool:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

            self.countryList = None

        def getSearch(self, query: str, exchange: str = None, limit: int = None):
            """
            Search:

            https://financialmodelingprep.com/developer/docs/stock-ticker-symbol-lookup-api

            Search stocks that are in our API by company name or ticker. You can also use the exchange filter to narrow
            down your results. Company name, currency, and exchange are some of the fields that are returned by API.

            Parameter           data type           example
            query               str                 'AA'
            exchange            str                 'ETF'
            limit               int                 20
            """

            # Check input parameters
            if exchange not in ['ETF', 'MUTUAL_FUND', 'COMMODITY', 'INDEX', 'CRYPTO', 'FOREX', 'TSX', 'AMEX', 'NASDAQ',
                                'NYSE', 'EURONEXT', 'XETRA', 'NSE', 'LSE', None]:
                raise ValueError('Parameter "exchange" can only be one of the following: \n'
                                 "['ETF', 'MUTUAL_FUND', 'COMMODITY', 'INDEX', 'CRYPTO', 'FOREX', 'TSX', 'AMEX',"
                                 "'NASDAQ', 'NYSE', 'EURONEXT', 'XETRA', 'NSE', 'LSE']")

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/search?query={QUERY}&apikey={YOUR_API_KEY}'.format(
                QUERY=query, YOUR_API_KEY=self.parent.API_KEY)
            # Append exchange to url if available
            if exchange:
                url = url + '&exchange={EXCHANGE}'.format(EXCHANGE=exchange)
            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getTickerSearch(self, query: str, exchange: str = None, limit: int = None):
            """
            Ticker Search:

            https://financialmodelingprep.com/developer/docs/stock-ticker-symbol-lookup-api

            Search stocks that are in our API by company name or ticker. You can also use the exchange filter to narrow
            down your results. Company name, currency, and exchange are some of the fields that are returned by API.

            Parameter           data type           example
            query               str                 'AA'
            exchange            str                 'ETF'
            limit               int                 20
            """

            # Check input parameters
            if exchange not in ['ETF', 'MUTUAL_FUND', 'COMMODITY', 'INDEX', 'CRYPTO', 'FOREX', 'TSX', 'AMEX', 'NASDAQ',
                                'NYSE', 'EURONEXT', 'XETRA', 'NSE', 'LSE', None]:
                raise ValueError('Parameter "exchange" can only be one of the following: \n'
                                 "['ETF', 'MUTUAL_FUND', 'COMMODITY', 'INDEX', 'CRYPTO', 'FOREX', 'TSX', 'AMEX',"
                                 "'NASDAQ', 'NYSE', 'EURONEXT', 'XETRA', 'NSE', 'LSE']")

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/search-ticker?query={QUERY}&apikey={YOUR_API_KEY}'.format(
                QUERY=query, YOUR_API_KEY=self.parent.API_KEY)
            # Append exchange to url if available
            if exchange:
                url = url + '&exchange={EXCHANGE}'.format(EXCHANGE=exchange)
            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getStockScreener(self, marketCapMoreThan: float = None, marketCapLowerThan: float = None,
                             priceMoreThan: float = None, priceLowerThan: float = None, betaMoreThan: float = None,
                             betaLowerThan: float = None, volumeMoreThan: float = None, volumeLowerThan: float = None,
                             dividendMoreThan: float = None, dividendLowerThan: float = None, isEtf: bool = None,
                             isActivelyTrading: bool = None, sector: str = None, industry: str = None,
                             country: str = None, exchange: str = None, limit: int = None):
            """
            Stock Screener:

            https://financialmodelingprep.com/developer/docs/stock-screener-api

            Stock screener is a more advanced way to search for stocks. Unlike our search endpoint, there is no query
            parameter, but there are numerous parameters such as market cap, price, volume, beta, sector, country, and
            so on. For example, you can use this endpoint to find NASDAQ-listed software companies that pay dividends
            and have good liquidity.

            Parameter           data type           example
            marketCapMoreThan   float               145812335.2
            marketCapLowerThan  float               145812335.2
            priceMoreThan       float               145812335.2
            priceLowerThan      float               145812335.2
            betaMoreThan        float               145812335.2
            betaLowerThan       float               145812335.2
            volumeMoreThan      float               145812335.2
            volumeLowerThan     float               145812335.2
            dividendMoreThan    float               145812335.2
            dividendLowerThan   float               145812335.2
            isEtf               bool                True
            isActivelyTrading   bool                True
            sector              str                 'Communication Services'
            industry            str                 'Banks'
            country             str                 'US'
            exchange            str                 'nasdaq'
            limit               int                 20
            """

            # Check input parameters
            if sector not in [None, 'Consumer Cyclical', 'Energy', 'Technology', 'Industrials', 'Financial Services',
                              'Basic Materials', 'Communication Services', 'Consumer Defensive', 'Healthcare',
                              'Real Estate', 'Utilities', 'Industrial Goods', 'Financial', 'Services', 'Conglomerates']:
                raise ValueError('Parameter "sector" can only be one of the following: \n'
                                 "['Consumer Cyclical', 'Energy', 'Technology', 'Industrials', 'Financial Services', "
                                 "'Basic Materials', 'Communication Services', 'Consumer Defensive', 'Healthcare', "
                                 "'Real Estate', 'Utilities', 'Industrial Goods', 'Financial', 'Services', 'Conglomerates']")

            if industry not in [None, 'Autos', 'Banks', 'Banks Diversified', 'Software', 'Banks Regional',
                                'Beverages Alcoholic', 'Beverages Brewers', 'Beverages Non-Alcoholic']:
                raise ValueError('Parameter "industry" can only be one of the following: \n'
                                 "['Autos', 'Banks', 'Banks Diversified', 'Software', 'Banks Regional', "
                                 "'Beverages Alcoholic', 'Beverages Brewers', 'Beverages Non-Alcoholic']")

            if exchange not in [None, 'nyse', 'nasdaq', 'amex', 'euronext', 'tsx', 'etf', 'mutual_fund']:
                raise ValueError('Parameter "exchange" can only be one of the following: \n'
                                 "['nyse', 'nasdaq', 'amex', 'euronext', 'tsx', 'etf', 'mutual_fund']")

            # Get country list
            if not self.countryList:
                self.countryList = self.parent.request('https://financialmodelingprep.com/api/v3/get-all-countries'
                                                       '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY))

            if country not in self.countryList and country is not None:
                raise ValueError('Parameter "country" can only be one of the following: \n' + ','.join(self.countryList))

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/stock-screener'
            query_list = []
            if marketCapMoreThan:
                query_list.append('marketCapMoreThan='+str(marketCapMoreThan))
            if marketCapLowerThan:
                query_list.append('marketCapLowerThan='+str(marketCapLowerThan))
            if priceMoreThan:
                query_list.append('priceMoreThan='+str(priceMoreThan))
            if priceLowerThan:
                query_list.append('priceLowerThan='+str(priceLowerThan))
            if betaMoreThan:
                query_list.append('betaMoreThan='+str(betaMoreThan))
            if betaLowerThan:
                query_list.append('betaLowerThan='+str(betaLowerThan))
            if volumeMoreThan:
                query_list.append('volumeMoreThan='+str(volumeMoreThan))
            if volumeLowerThan:
                query_list.append('volumeLowerThan='+str(volumeLowerThan))
            if dividendMoreThan:
                query_list.append('dividendMoreThan='+str(dividendMoreThan))
            if dividendLowerThan:
                query_list.append('dividendLowerThan='+str(dividendLowerThan))
            if isEtf is not None:
                query_list.append('isEtf='+str(isEtf))
            if isActivelyTrading is not None:
                query_list.append('isActivelyTrading='+str(isActivelyTrading))
            if sector:
                query_list.append('sector='+sector)
            if industry:
                query_list.append('industry='+industry)
            if country:
                query_list.append('country='+country)
            if exchange:
                query_list.append('exchange='+exchange)
            if limit:
                query_list.append('limit='+str(limit))

            query = '?' + '&'.join(query_list)
            url = url + query + '&apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

    class CompanyInformation:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getCompanyProfile(self, ticker: str):
            """
            Company Profile:

            https://financialmodelingprep.com/developer/docs/companies-key-stats-free-api

            Access data for a company such as 52 week high, 52 week low, market capitalization, and key stats to
            understand a company finance.
            Access companies profile (Price, Beta, Volume Average, Market Capitalisation, Last Dividend, 52 week range,
            stock price change, stock price change in percentage, Company Name, Exchange, Description, Industry, Sector,
            CEO,Website and image).
            The company profile endpoint allow to have a good overview of any company details.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/profile/{TICKER}?apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getKeyExecutives(self, ticker: str):
            """
            Key Executives:

            https://financialmodelingprep.com/developer/docs/key-executives

            Key executives are the people at the top of a company who make critical decisions that affect the company.
            We keep track of who they are, what their titles are, and how much money they make. We support the majority
            of companies because not everyone discloses all of their information.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/key-executives/{TICKER}?apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getMarketCapitalization(self, ticker: str):
            """
            Market Capitalization:

            https://financialmodelingprep.com/developer/docs/market-capitalization

            The value of a company is measured by its market capitalization. It's calculated by multiplying the price by
            the number of outstanding shares, both of which can be found on our quote endpoint. It's crucial in
            determining whether a company is undervalued, fairly valued or overvalued.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/market-capitalization/{TICKER}?apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getHistoricalMarketCapitalization(self, ticker: str, limit: int = None):
            """
            Historical Market Capitalization:

            https://financialmodelingprep.com/developer/docs/market-capitalization

            The value of a company is measured by its market capitalization. It's calculated by multiplying the price by
            the number of outstanding shares, both of which can be found on our quote endpoint. It's crucial in
            determining whether a company is undervalued, fairly valued or overvalued.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical-market-capitalization/{TICKER}?apikey=' \
                  '{YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getCompanyOutlook(self, ticker: str):
            """
            Company Outlook:

            https://financialmodelingprep.com/developer/docs/company-outlook

            Get the overview of any company. You will access its profile information, most insider trading transactions,
            financial statements in one API call.
            Accessing all of this information in one API call is very useful to get companies insight.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/company-outlook?symbol={TICKER}&apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getStockPeers(self, ticker: str):
            """
            Stock Peers:

            https://financialmodelingprep.com/developer/docs/stock-peers

            Stock peers are a group of companies that trade on the same exchange, are in the same industry (values can
            be found on our profile endpoint), and have a similar market capitalizations (which can be found on our
            market cap endpoint). All of our peers are based on stocks available through our API. This endpoint can be
            used to look up the competitors of a company you're interested in.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/stock_peers?symbol={TICKER}&apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getNYSETradingHours(self):
            """
            NYSE Holidays and Trading Hours:

            https://financialmodelingprep.com/developer/docs/is-the-market-open

            We support many markets, and this endpoint tells you which ones are open and which ones are closed. It
            returns the current state of the US market and EURONEXT. It also returns days when the stock market is
            closed, such as New Year's Day or Christmas.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/is-the-market-open?apikey={YOUR_API_KEY}'.format(
                YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getDelistedCompanies(self, limit: int = None):
            """
            Delisted Companies:

            https://financialmodelingprep.com/developer/docs/delisted-companies

            Access a list of delisted companies from the US exchanges.
            Stock delisting is the removal of a recorded stock from a stock trade exchange, and accordingly it would
            presently don't be exchanged on the bourse.

            Parameter           data type           example
            limit               int                 20
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/delisted-companies?apikey={YOUR_API_KEY}'.format(
                YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

    class StockNews:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getFMPArticles(self, page: int, size: int):
            """
            FMP Articles:

            https://financialmodelingprep.com/developer/docs/fmp-articles

            Access Financial Modeling Prep own proprietary articles written by our analysts. New articles are being
            created everyday. This endpoint contains fields like image, tickers, content and more.

            Parameter           data type           example
            page                int                 1
            size                int                 10
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/articles?page={PAGE}&size={SIZE}&apikey={YOUR_API_KEY}'.format(
                PAGE=page, SIZE=size, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getStockNews(self, tickers: str = None, limit: int = None):
            """
            Stock News:

            https://financialmodelingprep.com/developer/docs/stock-news

            It returns the most recent news with parameters like image or url of the original article. If you only want
            news about specific stocks, you can use the tickers parameter. Since 2017, we've kept track of everything
            that's happened.

            Parameters          Data type           example
            tickers             str                 'AAPL,FB,INTC'
            limit               int                 16
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/stock_news'
            query_list = []
            if tickers:
                query_list.append('tickers={TICKERS}'.format(TICKERS=tickers))
            if limit:
                query_list.append('limit={LIMIT}'.format(LIMIT=limit))

            query = '?' + '&'.join(query_list)
            url = url + query + '&apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getPressRelease(self, ticker: str, limit: int = None):
            """
            Press Release:

            https://financialmodelingprep.com/developer/docs/press-releases

            Companies usually communicate important information to the public through press releases. It could be a new
            product or financial results, for example. When they do this, we keep track of it and return the information
            from this endpoint.

            Parameters          Data type           example
            ticker              str                 'AAPL'
            limit               int                 16
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/press-releases/{TICKER}?limit={LIMIT}&apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, LIMIT=limit, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

    class MarketPerformace:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getSectorsPERatio(self, date: str = None, exchange: str = None):
            """
            Sector PE Ratio:

            https://financialmodelingprep.com/developer/docs/sectors-pe-ratio

            Our API calculates sector PE ratios from companies in a specific sector on a daily basis. You can use this
            to compare other companies to the average pe for their industry.

            Parameters          Data type           example
            date                str                 'YYYY-mm-dd'
            exchange            str                 'NYSE'
            """

            # Check input parameters
            if date:
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "date" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/sector_price_earning_ratio'
            query_list = []
            if date:
                query_list.append('date={DATE}'.format(DATE=date))
            if exchange:
                query_list.append('exchange={EXCHANGE}'.format(EXCHANGE=exchange))

            query = '?' + '&'.join(query_list)
            url = url + query + '&apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getIndustriesPERatio(self, date: str = None, exchange: str = None):
            """
            Industries PE Ratio:

            https://financialmodelingprep.com/developer/docs/industries-pe-ratio

            Industries The PE average is calculated using companies that are grouped by industry. This endpoint is
            updated on a daily basis, allowing you to look back at historical data. Divide the price by the earnings per
            share, or EPS, to get the price-to-earnings ratio, or PE.

            Parameters          Data type           example
            date                str                 'YYYY-mm-dd'
            exchange            str                 'NYSE'
            """

            # Check input parameters
            if date:
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "date" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/industry_price_earning_ratio'
            query_list = []
            if date:
                query_list.append('date={DATE}'.format(DATE=date))
            if exchange:
                query_list.append('exchange={EXCHANGE}'.format(EXCHANGE=exchange))

            query = '?' + '&'.join(query_list)
            url = url + query + '&apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getStockMarketSectorPerformance(self):
            """
            Stock Market Sectors Performance:

            https://financialmodelingprep.com/developer/docs/stock-market-sector-performance-free-api

            Check out performance by sector to see which one performs the best.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/stock/sectors-performance?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getHistoricalStockMarketSectorPerformance(self, limit: int = None):
            """
            Historical Stock Market Sectors Performance:

            https://financialmodelingprep.com/developer/docs/stock-market-sector-performance-free-api

            Check out performance by sector to see which one performs the best.

            Parameter           data type           example
            limit               int                 20
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical-sectors-performance?apikey={YOUR_API_KEY}'.format(
                YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getMostGainerStock(self):
            """
            Most Gainer Stock Companies:

            https://financialmodelingprep.com/developer/docs/most-gainers-stock-market-data-free-api

            The biggest percentage change in supported stocks returns the most gainers. As fields, it returns the
            ticker, name, change, and percentage change.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/gainers?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getMostLoserStock(self):
            """
            Most Loser Stock Companies:

            https://financialmodelingprep.com/developer/docs/most-losers-stock-market-data-free-api

            The most negative percent change of all supported stocks is returned by this endpoint. It returns ticker,
            name, change, and percentage change as fields. Normal stocks, mutual funds, etfs, and other securities can
            be among the tickers returned. As a result, 3X Bull/Bear ETFs may occasionally appear on the list.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/losers?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getMostActiveStock(self):
            """
            Most Active Stock Companies:

            https://financialmodelingprep.com/developer/docs/most-actives-stock-market-data-free-api/

            The most actively traded stocks are those with the highest volume of trades per day. This endpoint could be
            used to find hedge funds/mutual funds that are loading up on certain stocks or to find stocks that are
            trending today.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/actives?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

    class AdvancedData:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getStandardIndustrialClassification(self, ticker: str = None, industryTitle: str = None,
                                                cik: str = None,sic: str = None):
            """
            Standard Industrial Classification:

            https://financialmodelingprep.com/developer/docs/standard-industrial-classification

            SIC is a code given by US government to companies according to their business. Its mosly for US
            companies but also some other countries adopted this too. SIC is mostly used by SEC. It returns code
            but also the industry title.

            Parameter           data type           example
            ticker              str                 'AAPL'
            industryTitle       str                 'services'
            cik                 str                 '0000320193'
            sic                 str                 '3571'
            """

            # Generate url
            if ticker:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification?symbol=' \
                      '{TICKER}&apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)
            if industryTitle:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification?industryTitle=' \
                      '{INDUSTRY}&apikey={YOUR_API_KEY}'.format(INDUSTRY=industryTitle, YOUR_API_KEY=self.parent.API_KEY)
            elif cik:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification?cik=' \
                      '{CIK}&apikey={YOUR_API_KEY}'.format(CIK=cik, YOUR_API_KEY=self.parent.API_KEY)
            elif sic:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification?sicCode=' \
                      '{SIC}&apikey={YOUR_API_KEY}'.format(SIC=sic, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification/all?apikey' \
                      '={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getStandardIndustrialClassificationList(self, ticker: str = None, industryTitle: str = None,
                                                    cik: str = None, sic: str = None):
            """
            Standard Industrial Classification List:

            https://financialmodelingprep.com/developer/docs/standard-industrial-classification

            SIC is a code given by US government to companies according to their business. Its mosly for US
            companies but also some other countries adopted this too. SIC is mostly used by SEC. It returns code
            but also the industry title.

            Parameter           data type           example
            ticker              str                 'AAPL'
            industryTitle       str                 'services'
            cik                 str                 '0000320193'
            sic                 str                 '3571'
            """

            # Generate url
            if ticker:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification_list?symbol=' \
                      '{TICKER}&apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)
            if industryTitle:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification_list?industryTitle=' \
                      '{INDUSTRY}&apikey={YOUR_API_KEY}'.format(INDUSTRY=industryTitle, YOUR_API_KEY=self.parent.API_KEY)
            elif cik:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification_list?cik=' \
                      '{CIK}&apikey={YOUR_API_KEY}'.format(CIK=cik, YOUR_API_KEY=self.parent.API_KEY)
            elif sic:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification_list?sicCode=' \
                      '{SIC}&apikey={YOUR_API_KEY}'.format(SIC=sic, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v4/standard_industrial_classification_list?apikey' \
                      '={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCotTradingSymbolsList(self):
            """
            COT Trading Symbols List:

            https://financialmodelingprep.com/developer/docs/cot-symbols-list/

            You will be able to see all COT components individually to be able to call our the COT report API with
            specific symbols.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/commitment_of_traders_report/list?apikey={YOUR_API_KEY}'.format(
                YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCommitmentsOfTradersReport(self, ticker: str = None, from_: str = None, to_: str = None):
            """
            Commitments of Traders Report:

            https://financialmodelingprep.com/developer/docs/cot-reports

            The Commodity Futures Trading Commission (Commission or CFTC) publishes the Commitments of Traders (COT)
            reports to help the public understand market dynamics. Specifically, the COT reports provide a breakdown of
            each Tuesday’s open interest for futures and options on futures markets in which 20 or more traders hold
            positions equal to or above the reporting levels established by the CFTC.
            Generally, the data in the COT reports is from Tuesday and released Friday. The CFTC receives the data from
            the reporting firms on Wednesday morning and then corrects and verifies the data for release by Friday
            afternoon.

            Parameter           data type           example
            ticker              str                 'AAPL'
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if ticker and from_:
                raise ValueError('You can either use "ticker" or "from_"/"to_" parameter combo!')
            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError(
                        'Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            if from_ and to_:
                url = 'https://financialmodelingprep.com/api/v4/commitment_of_traders_report?from={FROM}' \
                      '&to={TO}&apikey={YOUR_API_KEY}'.format(FROM=from_, TO=to_, YOUR_API_KEY=self.parent.API_KEY)
            elif from_:
                url = 'https://financialmodelingprep.com/api/v4/commitment_of_traders_report?from={FROM}' \
                      '&apikey={YOUR_API_KEY}'.format(
                    FROM=from_, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v4/commitment_of_traders_report/' \
                      '{TICKER}?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCommitmentsOfTradersAnalysis(self, ticker: str = None, from_: str = None, to_: str = None):
            """
            Commitments of Traders Analysis:

            https://financialmodelingprep.com/developer/docs/cot-reports-analysis

            The Commitments of Traders (COT report) Analysis is a complete analysis of the COT reports.
            This analysis is done weekly as soon as the Commitments of Traders is published.

            Parameter           data type           example
            ticker              str                 'AAPL'
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if ticker and from_:
                raise ValueError('You can either use "ticker" or "from_"/"to_" parameter combo!')
            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError(
                        'Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            if from_ and to_:
                url = 'https://financialmodelingprep.com/api/v4/commitment_of_traders_report_analysis?from={FROM}' \
                      '&to={TO}&apikey={YOUR_API_KEY}'.format(FROM=from_, TO=to_, YOUR_API_KEY=self.parent.API_KEY)
            elif from_:
                url = 'https://financialmodelingprep.com/api/v4/commitment_of_traders_report_analysis?from={FROM}' \
                      '&apikey={YOUR_API_KEY}'.format(
                    FROM=from_, YOUR_API_KEY=self.parent.API_KEY)
            else:
                url = 'https://financialmodelingprep.com/api/v4/commitment_of_traders_report_analysis/' \
                      '{TICKER}?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)


    class StockStatistics:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getSocialSentiment(self, ticker: str, limit: int = None):
            """
            Social Statement:

            https://financialmodelingprep.com/developer/docs/social-sentiment

            With this endpoint, you can keep track of what people are saying about individual stocks on social media.
            Reddit, Yahoo, StockTwits, and Twitter are among the sites monitored. Absolute index field indicates how
            much people are talking about the stock, relative index also indicates it ​but relative to previous day.
            Sentiment field indicates overall percentage of positive activity, while general perception indicates
            whether people are more positive or negative than usual. This endpoint is updated with new data every hour,
            but it also contains previous data.

            Parameter           data type           example
            ticker              str                 'AAPL'
            limit               int                 20
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/social-sentiment?symbol={TICKER}&apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getStockGrade(self, ticker: str, limit: int = None):
            """
            Stock Grade:

            https://financialmodelingprep.com/developer/docs/stock-grade/

            This endpoint keeps track of the grades given to companies by hedge funds, investment firms and analysts.
            It includes both the previous and new grade. Because companies frequently maintain their grade, both of
            those fields can be the same at times.

            Parameter           data type           example
            ticker              str                 'AAPL'
            limit               int                 20
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/grade/{TICKER}?apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getEarningsSurprises(self, ticker: str):
            """
            Earnings Surprises:

            https://financialmodelingprep.com/developer/docs/earnings-surprises

            For stocks, this endpoint returns historical EPS earnings. It includes fields such as estimated and actual
            EPS.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/earnings-surprises/{TICKER}?apikey={YOUR_API_KEY}'.format(
                TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getAnalystEstimates(self, ticker: str, period: str = None, limit: int = None):
            """
            Stock Grade:

            https://financialmodelingprep.com/developer/docs/stock-grade/

            This endpoint keeps track of the grades given to companies by hedge funds, investment firms and analysts.
            It includes both the previous and new grade. Because companies frequently maintain their grade, both of
            those fields can be the same at times.

            Parameter           data type           example
            ticker              str                 'AAPL'
            period              str                 'quarter'
            limit               int                 20
            """

            # Check input parameters
            if period not in ['annual', 'quarter']:
                raise ValueError('Parameter "period" not specified correctly. Should be "annual" or "quarter"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/analyst-estimates/{TICKER}?period={PERIOD}&limit=30' \
                  '&apikey={YOUR_API_KEY}'.format(TICKER=ticker, PERIOD=period, YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

    class InsiderTrading:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getStockInsiderTrading(self, ticker: str = None, companyCik: str = None, reportingCik: str = None, limit: int = None):
            """
            Insider Trading:

            https://financialmodelingprep.com/developer/docs/stock-insider-trading

            We are getting insider trading informations from forms 3,4, and 5, which are filed with the SEC for each
            trade made by insiders. There are options, RSUs, and common stock included. Each item returned from the
            endpoint also has a price field, which indicates what price this transaction was filed at. The price can be
            0 if the company gave them stocks or options.

            Parameter           data type           example
            ticker              str                 'AAPL'
            companyCik          str                 '0000320193'
            reportingCik        str                 '0001214128'
            limit               int                 20
            """

            # Check input parameters
            notNoneCount = 0
            for input in [ticker, companyCik, reportingCik]:
                if input is not None:
                    notNoneCount += 1

            if notNoneCount > 1:
                raise ValueError('You can only use either "ticker", "companyCik" or "reportingCik" input parameter!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/insider-trading'

            if ticker:
                url = url + '?symbol=' + ticker
            elif companyCik:
                url = url + '?companyCik=' + companyCik
            elif reportingCik:
                url = url + '?reportingCik=' + reportingCik

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getCikMapper(self):

            # TODO: only supported with professional/enterprise api...

            return

        def getInsiderTradingRSSFeed(self, limit: int = None):
            """
            Insider Trading RSS Feed:

            https://financialmodelingprep.com/developer/docs/insider-trading-rss-feed

            This is an RSS feed for all market insider trading. It returns the most recent SEC Form 3, 4, and 5 filings,
            along with a link to the filing, the date, and other information.

            Parameter           data type           example
            limit               int                 20
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/insider-trading-rss-feed' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            # Append limit to url if available
            if limit:
                url = url + '&limit={LIMIT}'.format(LIMIT=limit)

            return self.parent.request(url)

        def getFailToDeliver(self, ticker: str):
            """
            Fail to deliver:

            https://financialmodelingprep.com/developer/docs/fail-to-deliver/

            This endpoint takes data from SEC page and is updated around every two weeks. Fail to deliver is when one
            party in trading contract doesn't deliver on their obligations. It returns days when it occured, price and
            quantity.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/fail_to_deliver?symbol={TICKER}' \
                  '&apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)


    class Prices:
        def __init__(self, parent):
            """
            Constructor

            Works for stocks, crypto, forex, comodities, etf, mutual funds prices
            """

            # Reference to parent class
            self.parent = parent

        def getQuote(self, tickers: str):
            """
            Quote:

            https://financialmodelingprep.com/developer/docs/stock-api

            The purpose of this endpoint is to quickly and easily obtain the most important company information. It
            includes fields such as the next earnings date, market cap, price, PE, EPS, and many more.

            Parameter           data type           example
            tickers              str                 'AAPL,FB,AMZN'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/quote/{TICKERS}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKERS=tickers, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getRealTimePrice(self, ticker: str):
            """
            Fail to deliver:

            https://financialmodelingprep.com/developer/docs/realtime-stock-quote-api#Stock-Real-time-Price

            This is a quick endpoint that only returns the stock price.
            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/quote-short/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getPriceList(self, exchange: str):
            """
            Fail to deliver:

            https://financialmodelingprep.com/developer/docs/realtime-stock-quote-api#Stock-Real-time-Price

            This is a quick endpoint that only returns the stock price.
            Parameter           data type           example
            exchange            str                 'nyse'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/quotes/{EXCHANGE}' \
                  '?apikey={YOUR_API_KEY}'.format(EXCHANGE=exchange, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getHistoricalPrices(self, ticker: str, timeframe: str):
            """
            Stock Historical Price:

            https://financialmodelingprep.com/developer/docs/historical-stock-data-free-api

            This endpoint provides access to historical prices that can be used to create charts. It's updated every day
            and can go back 15 years in time.

            Parameter           data type           example
            ticker              str                 'AAPL'
            timeframe           str                 '5min'
            """

            # Check input parameters
            if timeframe not in ['1min', '5min', '15min', '30min', '1hour', '4hour']:
                raise ValueError('Parameter "timeframe" not specified correctly. Should be "1min", "5min", "15min", '
                                 '"30min", "1hour" or "4hour"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical-chart/{TIMEFRAME}/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, TIMEFRAME=timeframe, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getHistoricalDailyPrices(self, tickers: str, seriesType: str, from_: str = None, to_: str = None,
                                     timeSeries: int = None):
            """
            Stock Historical Price:

            https://financialmodelingprep.com/developer/docs/historical-stock-data-free-api

            This endpoint provides access to historical prices that can be used to create charts. It's updated every day
            and can go back 15 years in time.You can also get a more than one stock with a single request, for
            example: historical-price-full/AAPL,FB.

            Parameter           data type           example
            tickers              str                 'AAPL,AMZN'     (multiple tickers are not supported by free api key,
                                                                    limited to 3, multiple stocks/mutual funds can only
                                                                    be queried if same exchange)
            from_               str                 'YYYY-mm-dd'
            to_                 str                 'YYYY-mm-dd'
            seriesType          str                 'line'|'bar'
            timeseries          int                 20              (returns data for the past "timeseries" days)
            """

            # Check input parameters
            if seriesType not in ['line', 'bar']:
                raise ValueError('Parameter "timeframe" not specified correctly. Should be "line" or "bar"!')

            if timeSeries and from_:
                raise ValueError('You can only use either "timeseries" or "from" parameter!')

            if to_ and not from_:
                raise ValueError('You must also specify "from_" parameter!')
            if from_:
                try:
                    datetime.datetime.strptime(from_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "from_" not specified correctly. Date should be in "YYYY-mm-dd" format!')
            if to_:
                try:
                    datetime.datetime.strptime(to_, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "to_" not specified correctly. Date should be in "YYYY-mm-dd" format!')



            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical-price-full/{TICKERS}'.format(TICKERS=tickers)
            query_list = []
            if seriesType:
                query_list.append('serietype=' + seriesType)
            if from_:
                query_list.append('from=' + from_)
            if to_:
                query_list.append('to=' + to_)
            if timeSeries:
                query_list.append('timeseries=' + str(timeSeries))


            query = '?' + '&'.join(query_list)
            url = url + query + '&apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getHistoricalDividends(self, ticker: str):
            """
            Historical Dividends:

            https://financialmodelingprep.com/developer/docs/historical-stock-dividends

            You can get dividend history for any stock, ETF, mutual fund, and more using this endpoint. Dividends are
            usually paid out every quarter, but they can also be paid out every month.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getHistoricalStockSplits(self, ticker: str):
            """
            Historical Stock Splits:

            https://financialmodelingprep.com/developer/docs/historical-stock-splits/

            This endpoint provides all historical stock splits for stocks with numerator and denominator fields. Stock
            splits affect both the price and the number of shares issued. If the company issues more shares, the price
            will become lower, but the overall value of the company will remain the same.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical-price-full/stock_split/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getSurvivorshipBiasFreeEod(self, ticker: str, date: str):
            """
            Survivorship Bias Free EOD:

            https://financialmodelingprep.com/developer/docs/survivorship-bias

            Obtain data such as the open, high, low, close, and volume for a specific stock and date.

            Parameter           data type           example
            ticker              str                 'AAPL'
            date                str                 'YYYY-mm-dd'
            """

            # Check input parameters
            if date:
                try:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                except ValueError:
                    raise ValueError('Parameter "date" not specified correctly. Date should be in "YYYY-mm-dd" format!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v4/historical-price-full/{TICKER}/{DATE}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, DATE=date, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getDailyIndicators(self, ticker: str, period: int, type: str):
            """
            Daily Indicators:

            https://financialmodelingprep.com/developer/docs/technicals-daily

            Daily technical indicators such as the SMA, EMA, and RSI are available, all options are displayed below. Use
            them to make advanced charts that will assist you in analyzing price changes or trading.

            Parameter           data type           example
            ticker              str                 'AAPL'
            period              int                 10
            type                str                 'sma'
            """

            # Check input parameters
            if type not in ['sma', 'ema', 'wma', 'dema', 'tema', 'williams', 'rsi', 'adx', 'standardDeviation']:
                raise ValueError('Parameter "type" not specified correctly. Should be "sma", "ema", "wma", "dema", '
                                 '"tema", "williams", "rsi", "adx" or "standardDeviation"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/technical_indicator/daily/{TICKER}?period={PERIOD}'\
                  '&type={TYPE}&apikey={YOUR_API_KEY}'.format(TICKER=ticker, PERIOD=period,
                                                              TYPE=type, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getIntradayIndicators(self, ticker: str, timeframe: str, period: int, type: str):
            """
            Intraday Indicators:

            https://financialmodelingprep.com/developer/docs/technicals-intraday

            Intraday technical indicators such as the SMA, EMA, and RSI are available, and they are updated every
            minute. Use them to make advanced charts that will assist you in analyzing price changes or trading.

            Parameter           data type           example
            ticker              str                 'AAPL'
            timeframe           str                 '5min'
            period              int                 10
            type                str                 'sma'
            """

            # Check input parameters
            if timeframe not in ['1min', '5min', '15min', '30min', '1hour', '4hour']:
                raise ValueError('Parameter "timeframe" not specified correctly. Should be "1min", "5min", "15min", '
                                 '"30min", "1hour" or "4hour"!')
            if type not in ['sma', 'ema', 'wma', 'dema', 'tema', 'williams', 'rsi', 'adx', 'standardDeviation']:
                raise ValueError('Parameter "type" not specified correctly. Should be "sma", "ema", "wma", "dema", '
                                 '"tema", "williams", "rsi", "adx" or "standardDeviation"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/technical_indicator/{TIMEFRAME}/{TICKER}?period={PERIOD}' \
                  '&type={TYPE}&apikey={YOUR_API_KEY}'.format(TICKER=ticker, TIMEFRAME=timeframe,PERIOD=period,
                                                              TYPE=type, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)


    class FundHoldings:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getEtfHolders(self, ticker: str):
            """
            ETF Holders:

            https://financialmodelingprep.com/developer/docs/etf-holders

            This endpoint returns all stocks held by a specific ETF. Assets, share number, and weight are among the
            fields returned. For example you can get components of SPY, VOO and more.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/etf-holder/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getInstitutionalHolders(self, ticker: str):
            """
            Institutional Holders:

            https://financialmodelingprep.com/developer/docs/institutional-holders/

            It provides information on institutional ownership of a specific stock. Fields like holder, shares, reported
            date, and change since previous report are all supported. The 13-F form, which requires institutions to
            report all of their assets, is primarily used to collect data. This endpoint can be used to keep track of
            how much a specific stock was bought or sold by institutions during a quarter.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/institutional-holder/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getMutualFundHolders(self, ticker: str):
            """
            Mutual Fund Holders:

            https://financialmodelingprep.com/developer/docs/mutual-fund-holders/

            This endpoint returns a list of all mutual fund holders for a given stock. 13-F forms from our SEC filings
            RSS endpoint are one of the sources of this. The endpoint returns fields such as shares and change weight
            percentage. This endpoint can be used to keep track of mutual funds activity.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/mutual-fund-holder/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getEtfSectorWeightings(self, ticker: str):
            """
            ETF Sector Weightings:

            https://financialmodelingprep.com/developer/docs/etf-sector-weightings/

            For each ETF we support, this endpoint returns the sector weight.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/etf-sector-weightings/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getEtfCountryWeightings(self, ticker: str):
            """
            ETF Country Weightings:

            https://financialmodelingprep.com/developer/docs/etf-country-weightings/

            This endpoint returns the ETF's country weight.

            Parameter           data type           example
            ticker              str                 'AAPL'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/etf-country-weightings/{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def get13FList(self):
            """
            13F List:

            Complete list of all institutional investment managers by cik.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/cik_list?apikey={YOUR_API_KEY}'.format(
                YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCikByCompanyName(self, companyName: str):
            """
            Search cik by name:

            FORM 13F cik search by name.

            Parameter           data type           example
            comapanyName        str                 'Berkshire'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/cik-search/{NAME}?apikey={YOUR_API_KEY}'.format(
                NAME=companyName, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCompanyNameByCik(self, cik: str):
            """
            Get company name by cik:

            FORM 13F get company name by cik.

            Parameter           data type           example
            cik                 str                 '0001067983'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/cik/{CIK}?apikey={YOUR_API_KEY}'.format(
                CIK=cik, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getForm13fByCik(self, cik: str, date: str):
            """
            Form 13F:

            FORM 13F statements provides position-level report of all institutional investment managers with more than
            $100m in assets under management.

            Parameter           data type           example
            cik                 str                 '0001067983'
            date                str                 '2020-06-30'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/form-thirteen/{CIK}?date={DATE}&apikey={YOUR_API_KEY}'.format(
                CIK=cik, DATE=date, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getFilingDatesByCik(self, cik: str):
            """
            Form 13F:

            13F Filings Dates by cik.

            Parameter           data type           example
            cik                 str                 '0001067983'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/form-thirteen-date/{CIK}?apikey={YOUR_API_KEY}'.format(
                CIK=cik, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getCusipMapper(self, cusip: str):
            """
            Cussip mapper

            Parameter           data type           example
            cusip               str                 '0001067983'
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/cusip/{CUSIP}?apikey={YOUR_API_KEY}'.format(
                CUSIP=cusip, YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)


    class StockList:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getSymbolsList(self):
            """
            Symbols List:

            https://financialmodelingprep.com/developer/docs/stock-market-quote-free-api/

            A list of all traded and non-traded stocks within our API. Symbol, name, price are all included for each
            company on the list. Our API contains over 25000 stocks.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/stock/list' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getTradableSymbolsList(self):
            """
            Tradable Symbols List:

            https://financialmodelingprep.com/developer/docs/tradable-list/

            A list of all actively traded stocks within our API. Symbol, name, price, and exchange are all included for
            each company on the list. Our API contains over 25000 stocks.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/available-traded/list' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getEtfList(self):
            """
            ETF List:

            https://financialmodelingprep.com/developer/docs/etf-list/

            It lists all of the ETFs that we support, as well as their names and prices. You can use it to see if the
            ETF you're looking for is one we support. Data such as sector weight, holders and historical prices are
            available for all ETFs in our API.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/etf/list' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)


    class BulkAndBatch:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        # TODO: only supported with professional/enterprise api...


    class MarketIndexes:
        def __init__(self, parent):
            """
            Constructor
            """

            # Reference to parent class
            self.parent = parent

        def getHistoricalSandP500ConstituentsList(self):
            """
            Historical S&P 500 constituents List:

            https://financialmodelingprep.com/developer/docs/historical-sp-500-companies-api

            This endpoint returns the history of S&P 500 securities that have been removed or added. It includes fields
            such as symbol, date, and reason, among others. You could use it in conjunction with our historical prices
            endpoint to see how these stocks' prices changed after they were added or removed.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical/sp500_constituent' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getListOfNasdaq100Companies(self):
            """
            List of Nasdaq 100 companies:

            https://financialmodelingprep.com/developer/docs/list-of-nasdaq-companies/

            Returns Companies in the Nasdaq 100, such as DocuSign and Zoom.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/nasdaq_constituent' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getListOfDowJonesCompanies(self):
            """
            List of Dow Jones companies:

            https://financialmodelingprep.com/developer/docs/list-of-dow-companies/

            Returns Companies in the Dow Jones, such as Honeywell and Home Depot.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/dowjones_constituent' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getHistoricalDowJonesConstituentsList(self):
            """
            Historical Dow Jones constituents List:

            https://financialmodelingprep.com/developer/docs/historical-dow/

            This endpoint keeps track of securities that have been removed or added to the Dow Jones index, which is one
            of the largest in the world.
            """

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/historical/dowjones_constituent' \
                  '?apikey={YOUR_API_KEY}'.format(YOUR_API_KEY=self.parent.API_KEY)

            return self.parent.request(url)

        def getSymbolList(self, ticker_type: str):
            """
            Symbol list:

            Returns different types of list of tickers.

            Parameter           data type           example
            ticker_type         str                 'cryptocurrencies'
            """

            #Check input parameters
            if ticker_type not in ['euronext', 'tsx', 'cryptocurrencies', 'forex-currency-pairs', 'commodities',
                          'etfs', 'mutual-funds', 'indexes', 'stocks']:
                raise ValueError('Parameter "statement_type" not specified correctly. Should be "euronext", "tsx", '
                                 '"cryptocurrencies", "forex-currency-pairs", "commodities", "etfs", "mutual-funds", '
                                 '"indexes" or "stocks"!')

            # Generate url
            url = 'https://financialmodelingprep.com/api/v3/symbol/available-{TICKER}' \
                  '?apikey={YOUR_API_KEY}'.format(TICKER=ticker_type, YOUR_API_KEY=self.parent.API_KEY)

