import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# data from crawler module
import news_crawler
# call to create a list with all available fetchers
articles = news_crawler.FetchList()
# app call
app = dash.Dash()

# app layout
# 
colors = {'background':'#111111','text':'#ffffff'} # nice way of org. colors
article_style = dict(width = '20%', verticalAlign='top',
    color = colors['text'], display='inline-block')

def create_provider_layout(providers):
    html_out = {}
    for news_provider in providers:
        html_out[news_provider] = html.Div([html.H1(providers[news_provider]),
        html.Details([html.Summary('See all:'),
            dcc.Markdown(id=news_provider)], open = True )],
        style = article_style)
    return html_out

# layout
# this maybe confusing but useful, if more news providers are added to the news feed
# the individual layout off each provider is created by the 'create_provider_layout()' 
# this returns a dictonary of created html, this way it could be added to the app layout 
# by passing the key like: provider_layout['ny']

providers = {'ny':'NY-Times', 'rt':'Russia Today', 'bbc':'BBC', 'aj':'Aljazeera'}
provider_layout = create_provider_layout(providers)
app.layout = html.Div([
    html.Button(id='submit_bttn',
                n_clicks=0,
                children='Update',
                style=dict(fontSize='24')),  # add a submmit button
    provider_layout['ny'],
    provider_layout['rt'],
    provider_layout['bbc'],
    provider_layout['aj'],
], style = dict(backgroundColor = colors['background']))

# callbacks for interactivity
@app.callback(Output('ny', 'children'),
              [Input('submit_bttn', 'n_clicks')])
def output(n):
    ny_text = ''
    for article in articles.fetch_all(keys =['ny']):
        ny_text = ny_text + "\n" + article.to_markdown().content
    return ny_text

@app.callback(Output('rt', 'children'),
              [Input('submit_bttn', 'n_clicks')])
def output_rt(n):
    rt_text = ''
    for article in articles.fetch_all(keys =['rt']):
        rt_text = rt_text + "\n" + article.to_markdown().content
    return rt_text

@app.callback(Output('bbc', 'children'),
              [Input('submit_bttn', 'n_clicks')])
def output_bbc(n):
    bbc_text = ''
    for article in articles.fetch_all(keys =['bbc']):
        bbc_text = bbc_text + "\n" + article.to_markdown().content
    return bbc_text

@app.callback(Output('aj', 'children'),
              [Input('submit_bttn', 'n_clicks')])
def output_aj(n):
    aj_text = ''
    for article in articles.fetch_all(keys =['aj']):
        aj_text = aj_text + "\n" + article.to_markdown().content
    return aj_text


# run
if __name__ == '__main__':
    app.run_server()

