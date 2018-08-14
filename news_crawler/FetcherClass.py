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
            ref = element.select_one('a').attrs['href']
            if title and content is not None:
                yield NewsArticle(title=title.text.strip(),
                                  content=content.text.strip(),
                                  ref=ref,
                                  type="NyTimes")


class RtFetcher(Fetcher):
    def __init__(self, con):
        super(RtFetcher, self).__init__(con)  # this redundant atm

    def fetch(self):
        # get fetcher method
        doc = super(RtFetcher, self).fetch()
        counter = 0
        for element in doc.select('.card'):
            counter += 1
            title = element.select_one('.card__header')
            content = element.select_one('.card__summary')
            ref = 'https://www.rt.com'+element.select_one('a').attrs['href']
            if content is not None and title is not None and counter <= 10:
                yield NewsArticle(title=title.text.strip(),content=content.text.strip(),
                                  ref = ref,
                                  type='RT')


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
                ref ='https://www.bbc.com'+element.select_one('a').attrs['href']
                yield NewsArticle(title=element.select_one(".gs-c-promo-heading").text,
                                  ref = ref,
                                  content=content.text, type="BBC")


# other fetchers not implemented yet

class AJFetcher(Fetcher): # this fetcher is quite ugly
    def __init__(self, con):
        super(AJFetcher, self).__init__(con)  # this redundant atm

    def fetch(self):
        # get fetcher method
        doc = super(AJFetcher, self).fetch()

        for element in doc.select('.topics-sec-block'):
                    titles = element.find_all('h2')
                    content = element.find_all('p', attrs = {'class' : 'topics-sec-item-p'})
                    ref = element.find_all('a', attrs={'class': None}, href=True)
                    seq = range(len(ref))
                    ref_list = [ref[r].attrs['href'] for r in seq[0::2]] # entries are doubled, thats why slicing
                    
                    for i in range(len(titles)):
                        yield NewsArticle(title=titles[i].text,
                        content=content[i].text, type= 'AJ', ref = 'https://www.aljazeera.com/'+ref_list[i])

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




