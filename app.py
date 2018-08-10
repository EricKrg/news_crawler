import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State


# data from crawler module
import news_crawler

articles = news_crawler.FetchList()
# app call
app = dash.Dash()

# app layout
# start off with three divs
colors = {'background':'#111111','text':'#ffffff'} # nice way of org. colors
article_style = dict(width = '30%', verticalAlign='top',
    color = colors['text'], display='inline-block')

app.layout = html.Div([
    html.Button(id='submit_bttn',
                n_clicks=0,
                children='Update',
                style=dict(fontSize='24')),  # add a submmit button
    html.Div([html.H1('NY-Times'),
        dcc.Markdown(id='ny')],style = article_style),
    html.Div([html.H1('Russia Today'),
        dcc.Markdown(id = 'rt')], style = article_style),
    html.Div([html.H1('BBC'),
        dcc.Markdown(id = 'bbc')], style = article_style)
], style = dict(backgroundColor = colors['background']))

# callbacks for interactivity
@app.callback(Output('ny', 'children'),
              [Input('submit_bttn', 'n_clicks')])
def output(n):
    ny_text = ''
    for article in articles.article_list(keys =['ny']):
        ny_text = ny_text + "\n" + article.to_markdown().content
    return ny_text

@app.callback(Output('rt', 'children'),
              [Input('submit_bttn', 'n_clicks')])
def output_rt(n):
    rt_text = ''
    for article in articles.article_list(keys =['rt']):
        rt_text = rt_text + "\n" + article.to_markdown().content
    return rt_text

@app.callback(Output('bbc', 'children'),
              [Input('submit_bttn', 'n_clicks')])
def output_bbc(n):
    bbc_text = ''
    for article in articles.article_list(keys =['bbc']):
        bbc_text = bbc_text + "\n" + article.to_markdown().content
    return bbc_text



# run
if __name__ == '__main__':
    app.run_server()

