import news_crawler

# fetch all articles

list = news_crawler.FetchList()
#print(list)

for news in list.article_list():
    print(news.type)
    print(news.show())
    print('\n')