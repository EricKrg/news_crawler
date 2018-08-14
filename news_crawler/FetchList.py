from .FetcherClass import *
#---------------------------------------------------------------------------
# atm i provide the link to the news webpage as statics in ths class,
# this way i only have to create a FetchList and call the article list function 
# to get all articles from this side
class FetchList(object):
    def __init__(self):
        self.fetchers = {
            'rt':RtFetcher("https://www.rt.com/news"),
            'ny':NyTimesFetcher("https://www.nytimes.com/"),
            'bbc':BBCFetcher("https://www.bbc.com/news"),
            'aj':AJFetcher('https://www.aljazeera.com/news/')
        }
    def fetch_all(self, keys):
        art_list = []
        for key in keys:
            for article in self.fetchers[key].fetch():
                art_list.append(article)
        return art_list

