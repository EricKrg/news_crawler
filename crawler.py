import news_crawler

fetcher_list = [
    news_crawler.RtFetcher("https://www.rt.com/news"),
    news_crawler.NyTimesFetcher("https://www.nytimes.com/"),
    news_crawler.BBCFetcher("https://www.bbc.com/news")
]

i = 0

for fetcher in fetcher_list:
    for article in fetcher.fetch():
        i += 1
        article.show()
        print "\n"