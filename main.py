from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# raw url to specify ticker
finviz_url="https://finviz.com/quote.ashx?t="

tickers=['AMZN', 'AMD', 'FB']
news_tables={}

# using BeautifulSoup to parse finviz
for ticker in tickers:
    url = finviz_url + ticker

    # header allows to access data
    req = Request(url=url, headers={'user-agent': 'nlp-app'})
    response = urlopen(req)

    html = BeautifulSoup(response, 'html')
    news_table = html.find(id='news-table')
    news_tables[ticker] = news_table

    break

# store all data from all tickers
parsed_data = []
for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.get_text()  # looking for anchor tag and access the text
        # debugging weird timestamp formatting
        date_time = row.td.text.replace('\r\n',' ').split(' ')[13:15]

        # date_time either contains both datea and time or only time of the same day
        if len(date_time[1]) < 3:
            time = date_time[0]
        else:
            date = date_time[0]
            time = date_time[1]

        parsed_data.append([ticker, date, time, title])

print(parsed_data)
        