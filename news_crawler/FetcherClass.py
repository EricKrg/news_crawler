import requests
from .NewsArticle import NewsArticle
from bs4 import BeautifulSoup

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urljoin


# ---------------------------------------

# parent fetcher
class Fetcher(object):
    def __init__(self, con):
        self.con = con

    def fetch(self):
        r = requests.get(self.con)
        return BeautifulSoup(r.text, "html.parser")


class NyTimesFetcher(Fetcher):
    def __init__(self, con):
        super(NyTimesFetcher, self).__init__(con)  # this redundant atm

    def fetch(self):
        # get fetcher method
        doc = super(NyTimesFetcher, self).fetch()

        for element in doc.select(".top-news .a-column .collection"):
            title = element.select_one(".story-heading")
            content = element.select_one(".summary")
            if title and content is not None:
                yield NewsArticle(title=title.text.strip(),
                                  content=content.text.strip(),
                                  type="NyTimes")


class RtFetcher(Fetcher):
    def __init__(self, con):
        super(RtFetcher, self).__init__(con)  # this redundant atm

    def fetch(self):
        # get fetcher method
        doc = super(RtFetcher, self).fetch()
        counter = 0
        for element in doc.select(".card"):
            counter += 1
            title = element.select_one(".card__header")
            content = element.select_one(".card__summary")
            if content is not None and title is not None and counter <= 10:
                yield NewsArticle(title=title.text.strip(), content=content.text.strip(),
                                  type="RT")


class BBCFetcher(Fetcher):
    def __init__(self, con):
        super(BBCFetcher, self).__init__(con)  # this redundant atm

    def fetch(self):
        # get fetcher method
        doc = super(BBCFetcher, self).fetch()

        counter = 0
        for element in doc.select(".gs-c-promo"):
            counter += 1
            content = element.select_one(".gs-c-promo-summary")
            if content is not None and counter <= 10:
                yield NewsArticle(title=element.select_one(".gs-c-promo-heading").text,
                                  content=content.text, type="BBC")


# other fetchers not implemented yet
class WpFetcher(object):
    def __init__(self, con):
        super(WpFetcher, self).__init__(con)  # this redundant atm

    def fetch(self):
        # get fetcher method
        doc = super(WpFetcher, self).fetch()

    pass


class SunFetcher(object):
    def __init__(self, con):
        self.con = con

    pass



#---------------------------------------------------------------------------
# atm i provide the link to the news webpage as statics in ths class,
# this way i only have to create a FetchList and call the article list function 
# to get all articles from this side
class FetchList(object):
    def __init__(self):
        self.fetchers = {
            'rt':RtFetcher("https://www.rt.com/news"),
            'ny':NyTimesFetcher("https://www.nytimes.com/"),
            'bbc':BBCFetcher("https://www.bbc.com/news")
        }
    def article_list(self, keys):
        art_list = []
        for key in keys:
            for article in self.fetchers[key].fetch():
                art_list.append(article)
        return art_list

