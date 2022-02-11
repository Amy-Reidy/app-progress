import pandas as pd
import numpy as np

## Dash
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import flask

## Page Imports
from app1 import App1, build_graph
from app2 import App2, get_datatable
from app3 import App3, get_chart 
from homepage import Homepage

# Dash Instance --------------------------------------------------------------------------------------
server = flask.Flask(__name__) # define flask app.server
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.FLATLY]) 
app.title = 'LP Analytics'
app._favicon = './assets/images/favicon.ico'
app.config.suppress_callback_exceptions = True

# Data for table --------------------------------------------------------------------------------------

df = pd.read_csv('./assets/data/data_with_regions.csv')
country_list = df['Country'].unique()
# turn country column into a hyperlink
df['Country'] = '['+df['Country']+']'+'(https://lotus-project.s3.us-east-2.amazonaws.com/RDM+Index/'+df['Country'].str.replace(" ", "%20")+".zip)"


# App Layout - Look at script for each app for each page's layout -------------------------------------

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
    ])

# ------Callbacks ------------------------------------------------------------------------------------

# Overall App Callbacks -------------------------------------------------------------------------------

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/time-series':
        return App1()
    elif pathname == '/download-data':
        return App2()
    elif pathname == '/WBI':
        return App3()
    else:
        return Homepage()

# App 1 Callbacks ------------------------------------------------------------------------------------

@app.callback(
    Output('output', 'children'),
    [Input('pop_dropdown', 'value')])   
def update_graph(city):
    graph = build_graph(city)
    return graph


# App 2 Callbacks ------------------------------------------------------------------------------------

# Callback to update datatable

@app.callback(
    Output('data-table-div', 'children'),
    [Input('filter', 'value'),
    Input('radio_item', 'value')])   
def filter_table(filter, radio_item):  
  if filter == 'all_values':
    return get_datatable(df.to_dict('records'))

  elif radio_item == 'Sub-Region':
    subregion_filtered_df = df[df['Sub-Region'] == filter]      
    return get_datatable(subregion_filtered_df.to_dict('records'))

  elif radio_item == 'Region':
    subregion_filtered_df = df[df['Region'] == filter]      
    return get_datatable(subregion_filtered_df.to_dict('records'))

  elif radio_item == 'Country':
    country_filtered_df = df[df['Country'].str.startswith('[{}'.format(filter))]      
    return get_datatable(country_filtered_df.to_dict('records'))   
  
  else:
    country_filtered_df = df[df['Country'].str.startswith('[{}'.format(filter))]      
    return get_datatable(country_filtered_df.to_dict('records'))


# Callback to update searchbox based on radio items

@app.callback([
    Output('filter', 'options'),
    Output('filter', 'value')],
    [Input('radio_item', 'value')])
def update_dropdown(radio_item):
  if radio_item == 'Country':
    return [{'label': 'Select all', 'value': 'all_values'}] + [{'label': i, 'value': i} for i in country_list], 'all_values'
  elif radio_item == 'Sub-Region':
    return [{'label': 'Select all', 'value': 'all_values'}] + [{'label': i, 'value': i} for i in np.sort(df['Sub-Region'].unique())], 'all_values'
  else:
    return [{'label': 'Select all', 'value': 'all_values'}] + [{'label': i, 'value': i} for i in np.sort(df['Region'].unique())], 'all_values'


# App 3 Callbacks ------------------------------------------------------------------------------------

# Callback to update bubble chart

@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('x-axis', 'value'),
     Input('y-axis', 'value')])
def update_chart(xaxis, yaxis):
    fig = get_chart(xaxis, yaxis)
    return fig


 # -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=False)