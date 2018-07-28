class NewsArticle(object):
    def __init__(self, title, content, type):
        self.title = title
        self.content = content
        self.type = type

    def show(self):
        print(self.title)
        print(self.content)
        print(self.type)
