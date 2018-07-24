import requests
from .NewsArticle import NewsArticle
from bs4 import BeautifulSoup

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urljoin


# ---------------------------------------

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
                yield NewsArticle(title=title.text.strip(), content=content.text.strip())


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
