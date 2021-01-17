#!/usr/local/bin/venv python3

import pandas as pd
import numpy as np
import datetime
import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

DIR = '/content/drive/MyDrive/ai/machine_learning/superstore-sales-analysis/'
df = pd.read_excel(f'{DIR}superstore_sales.xlsx')

def category():
  df_cat = df.groupby('category')['profit'].sum().reset_index()
  df_cat.sort_values(by=['profit'], ascending=False)
  return html.Div([
    html.P('Most Profitable Category', 
        style={'text-align':'center', 'color':'white'}),

    dcc.Graph(figure = px.pie(df_cat, values='profit', names='category', labels={'profit':'Profit'}).update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, font={'color':'#839496'}), style={'height':'373px'}, config={'displayModeBar': False})
  ])
  
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],
                meta_tags=[{'name':'viewport',
                'content':'width=device-width, initial-scale=1.0'}])

app.layout = dbc.Container([
    dbc.Row(
        dbc.Col(
                html.H2('Super Store Dashboard', style={'color':'white', 'padding-top':'20px', 'padding-bottom':'30px'}, className='text-center lg-4'), 
                xs=12, sm=12, md=12, lg=12, xl=12)
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.P('Most Profitable Sub Category by Region', style={'color':'white'}, className='text-center lg-6'),

                    dbc.RadioItems(id='radio_sub', value='Sub Category', className='text-center',
                            options=[{'label':'Sub Category', 'value':'Sub Category'}, {'label':'Region', 'value':'Region'},], inline=True),

                    dcc.Graph(id='sub_fig', config={'displayModeBar': False}, style={'height':'350px'}, className='text-center')
                ]), className='col-con'
            )
            
        ], xs=12, sm=12, md=12, lg=4, xl=4),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    category()
                    ]), className='col-con'
            )
        ], xs=12, sm=12, md=12, lg=5, xl=5),

        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    category()
                    ]), className='col-con'
            )
        ],xs=12, sm=12, md=12, lg=3, xl=3),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.graph(id='overall-sales')
                ]), className='col-con'
            ])
        ], xs=12, sm=12, md=12, lg=12, xl=12),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.graph()
                ]), className='col-con'
            ])
        ], xs=12, sm=12, md=12, lg=12, xl=12),
    ])
], fluid=True)

# Define callback to update graph
@app.callback(Output('sub_fig', 'figure'),
              Input('radio_sub', 'value'))

def update_graph(radio_sub):
  most_profit_sub = df.groupby('sub_category')[['profit', 'product_name']].sum().reset_index()
  sub_top_profit= most_profit_sub.sort_values(by=['profit'], ascending=False).iloc[0:10]
  region = df.groupby(['year', 'segment', 'region'])['profit'].sum().reset_index()
  region_top = region.sort_values(by=['profit'], ascending=False).iloc[0:10]

  if radio_sub == 'Sub Category':
      fig = px.bar(sub_top_profit, x='sub_category', y='profit', 
                  color='sub_category', labels={'sub_category':'Sub Category', 'profit':'Profit'})
      fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, 
                        xaxis=dict(showgrid=True), yaxis=dict(showgrid=True), font={'color':'#839496'})
      return fig

  elif radio_sub == 'Region':
      fig = px.bar(region_top, x='region', y='profit', 
                  color='region', labels={'region_top':'Region', 'profit':'Profit'})
      fig.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor':'rgba(0, 0, 0, 0)'}, 
                        xaxis=dict(showgrid=True), yaxis=dict(showgrid=True), font={'color':'#839496'})
      return fig


if __name__ == '__main__':
  app.run_server(debug=True)