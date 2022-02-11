from enum import auto
import pandas as pd
import numpy as np

## Dash
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

## Plotly
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_white"

## Navbar
from navbar import Navbar
nav = Navbar()

# ------------------------------------------------------------------------------
## Data + Dropdown Options
df = pd.read_csv('./assets/data/cervical_cancer_global_data.csv')

x_features = ['Human Development Index (HDI)', 'Life Expectancy at Birth',
       'Expected Years of Schooling', 'Mean Years of Schooling',
       'Gross National Income (GNI) per Capita', 'Incidence', 'Mortality']

y_features = ['Incidence', 'Mortality']

# ------------------------------------------------------------------------------
# Page Elements

header = html.H4('Bubble Chart of World Bank Index')

chart = html.Div([
        dcc.Graph(
          id="scatter-plot",
          config={'displayModeBar': False})
          ])


xaxis_dropdown = html.Div([
        dcc.Dropdown(
          id='x-axis', 
          options=[{'label': i.title(), 'value': i} for i in x_features], 
          value='Human Development Index (HDI)')
          ])

yaxis_dropdown = html.Div([        
        dcc.Dropdown(
          id='y-axis', 
          options=[{'label': i.title(), 'value': i} for i in y_features], 
          value='Incidence')
          ])

# ------------------------------------------------------------------------------
# Chart function

def get_chart(xaxis_name, yaxis_name):
      figure = px.scatter(df,
          x=xaxis_name,
          y=yaxis_name,
          color=df['Continent'],
          size=yaxis_name,
          opacity=0.7,
          height=600,
          hover_name="Country", hover_data={yaxis_name:True, xaxis_name:True}
          )
      figure.update_layout(title_text='{} Vs. {}'.format(yaxis_name.title(), xaxis_name.title()), title_x=0.5)        
      figure.update_layout(margin={"r":30,"t":50,"l":30,"b":0})
      figure.update_layout(legend=dict(
              title="Region",
              yanchor="top",
              y=0.99,
              xanchor="right",
              x=0.99))
      return figure 


# ------------------------------------------------------------------------------
# Page layout

def App3():
    layout = html.Div([
        nav,
        html.Div([
            html.Div(id='chart-div',
                    children=[chart],
                    style={'width':'80%', 'display':'inline-block'}),
            html.Div(id='sidebar',
                    children=[dcc.Tabs(id='sidebar-tabs',
                                      children=[
                                        dcc.Tab(id='about-tab',
                                                label='About',
                                                children=[html.Div([
                                                  html.Br(),
                                                  html.H6('What is WBI?'),
                                                  dcc.Markdown('Short paragraph explaining what WBI is with link to more information and instructions on how to use chart')],
                                                  style={'margin':'10px'})],
                                                  ),
                                        dcc.Tab(id='bubble-tab',
                                                label='Bubble Chart',
                                                children=[html.Div([
                                                  html.Br(),
                                                  html.H6('Choose x-axis'),
                                                  xaxis_dropdown,
                                                  dcc.Markdown('Short sentence here to describe indicator'),
                                                  html.Br(),
                                                  html.H6('Choose y-axis'),
                                                  yaxis_dropdown,
                                                  dcc.Markdown('Short sentence here to describe indicator')],
                                                  style={'margin':'10px'})],
                                                  ),
                                          dcc.Tab(id='map-tab',
                                                label='Map',
                                                children=[html.Div([
                                                  html.H6('Map options here')],
                                                  style={'margin':'10px'})],
                                                  )
                                ])
                            ],
                    style={'display':'inline-block', 'width':'20%', 'vertical-align':'top', "border":"1px #eeeeee solid", 'height':'600px'})
                ],
                style={'margin':'0px', 'padding':'5px'})
            ])
    return layout
