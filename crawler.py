import news_crawler

ny_fetch = news_crawler.NyTimesFetcher("https://www.nytimes.com/")

for article in ny_fetch.fetch():
    article.show()
    print "\n"


