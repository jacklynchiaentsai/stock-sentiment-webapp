from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt
import time

# raw url to specify ticker
finviz_url="https://finviz.com/quote.ashx?t="

tickers=['AMZN', 'GOOG']
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
    time.sleep(5)


# store all data from all tickers
parsed_data = []
for ticker, news_table in news_tables.items():
    for row in news_table.findAll('tr'):
        title = row.a.get_text()  # looking for anchor tag and access the text
        # debugging weird timestamp formatting
        date_time = row.td.text.replace('\r\n',' ').split(' ')[13:15]

        # date_time either contains both datea and time or only time of the same day
        if len(date_time[1]) < 3:
            dtime = date_time[0]
        else:
            date = date_time[0]
            dtime = date_time[1]

        parsed_data.append([ticker, date, dtime, title])

        
#using pretrained nltk.sentiment.vader to apply sentiment analysis
df = pd.DataFrame(parsed_data, columns=['ticker', 'date', 'time', 'title'])

# polarity scores based off of positive words or negative words -> some incorrect exceptions
model = SentimentIntensityAnalyzer()

# lambda function
f = lambda title: model.polarity_scores(title)['compound']
df['compound'] = df['title'].apply(f)
#print(df.head())

# converting date time to ordering (convert from string to date time format)
df['date'] = pd.to_datetime(df.date).dt.date

# using matplotlib to visualize data
plt.figure(figsize=(10,8))
# Create a new DataFrame grouped by 'ticker' and 'date', and calculate the mean of 'compound'
mean_df = df.groupby(['ticker', 'date']).agg(avg_score=('compound', 'mean')).reset_index()

# Sort the DataFrame by 'date' for better visualization
mean_df.sort_values(by='date', inplace=True)

# Plotting as bar chart
plt.figure(figsize=(10, 6))
width = 0.35
tickers = mean_df['ticker'].unique()
for i, ticker in enumerate(tickers):
    ticker_data = mean_df[mean_df['ticker'] == ticker]
    x = range(i, i + len(ticker_data))
    plt.bar(x, ticker_data['avg_score'], width=width, label=ticker)

plt.xlabel('Date')
plt.ylabel('Average Score')
plt.title('Average Score Change Over Time')
plt.xticks(range(len(mean_df['date'].unique())), mean_df['date'].dt.strftime('%Y-%m-%d').unique(), rotation=45)
plt.legend()
plt.grid(axis='y')
plt.tight_layout()
plt.show()





