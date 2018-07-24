
class NewsArticle(object):
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def show(self):
        print self.title
        print self.content

