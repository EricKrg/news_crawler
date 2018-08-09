import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# data from crawler module
import news_crawler
fetcher_list = [
    news_crawler.RtFetcher("https://www.rt.com/news"),
    news_crawler.NyTimesFetcher("https://www.nytimes.com/"),
    news_crawler.BBCFetcher("https://www.bbc.com/news")
]

# this is not here to stay 
bbc_text = rt_text = ny_text = ''
for fetcher in fetcher_list:
    for article in fetcher.fetch():
        if article.type == 'BBC':
            bbc_text = bbc_text + "\n" + article.to_markdown()
        if article.type == 'NyTimes':
            ny_text = ny_text + "\n" + article.to_markdown()
        if article.type == 'RT':
            rt_text = rt_text + "\n" + article.to_markdown()
    
# app call
app = dash.Dash()

# app layout
# start off with three divs
colors = {'background':'#111111','text':'#ffffff'} # nice way of org. colors
article_style = dict(width = '30%', verticalAlign='top',
    color = colors['text'], display='inline-block')

app.layout = html.Div([
    html.Div([html.H1('NY-Times'),
        dcc.Markdown(children = ny_text)],style = article_style),
    html.Div([html.H1('Russia Today'),
        dcc.Markdown(children = rt_text)], style = article_style),
    html.Div([html.H1('BBC'),
        dcc.Markdown(children = bbc_text)], style = article_style)
], style = dict(backgroundColor = colors['background']))

# callbacks for interactivity

# run
if __name__ == '__main__':
    app.run_server()

