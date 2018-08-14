class NewsArticle(object):
    def __init__(self, title, content, type, ref):
        self.title = title
        self.content = content
        self.ref = ref
        self.type = type

    def show(self):
        print(self.title)
        print(self.content)
        print(self.type)

    def to_markdown(self):
        return MarkdownArticle('### ' + self.title + '\n' + self.content + '[*Full Text*]' +'('+self.ref+')') 
 
class MarkdownArticle(object):
    def __init__(self,content):
        self.content = content
