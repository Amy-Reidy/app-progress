import pandas as pd
import numpy as np

## Dash
from dash import Dash, html, dash_table, dcc
from dash import dash_table 
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


## Navbar
from navbar import Navbar
nav = Navbar()


# ------------------------------------------------------------------------------
# Data, country options for searchbox and country hyperlink.

df = pd.read_csv('./assets/data/data_with_regions.csv')
country_list = df['Country'].unique()
# turning country column into a hyperlink
df['Country'] = '['+df['Country']+']'+'(https://lotus-project.s3.us-east-2.amazonaws.com/RDM+Index/'+df['Country'].str.replace(" ", "%20")+".zip)"



# ------------------------------------------------------------------------------
# Page elements

header = html.H3('Download Raw RDM Suitability Index Data')

search_by =  html.Div([html.H6('Search by:')], id='search_by')

radio_items = html.Div([
                dcc.RadioItems(
                  id='radio_item', 
                  options=[
                    {'label':'  Country', 'value':'Country'},
                    {'label':'  Sub-Region', 'value':'Sub-Region'},
                    {'label':'  Region', 'value':'Region'}],
                  value='Country',
                  labelStyle={'display':'inline-block', 'margin-left':'10px', 'margin-right':'5px'})],
                  id='radio_div')

dropdown =  html.Div([               
              dcc.Dropdown(
                id='filter',
                options= [
                {'label': 'Select all', 'value': 'all_values'}] + [{'label': i, 'value': i} for i in country_list],
                value='all_values',
                clearable=False)],
                style = {'verticalAlign': 'bottom'},
                id='filter_div')

table = html.Div(id="data-table-div", 
                  children=[],
                  )

# ------------------------------------------------------------------------------
# Table Function

def get_datatable(table_data):
      data_table = dash_table.DataTable(
                        id='data_table',
                        columns=[{'id': x, 'name': x,'presentation':'markdown'} if x == 'Country' else {'id': x, 'name': x} for x in df.columns],
                        data=table_data,
                        fixed_rows={'headers': True},
                        style_table={'height': 470},  
                        style_cell={'fontFamily': 'Libre Franklin, sans-serif',
                                  'padding':'10px 0px 10px 10px',
                                  'textAlign':'left', 'verticalAlign':'top'},
                        style_header={'fontWeight':'600', 'padding':'10px 0px 10px 10px'},
                        style_as_list_view=True,
                        style_data={'whiteSpace':'normal'},
                        style_cell_conditional=[
                                {'if': {'column_id': 'Country'},'width': '23%'},
                                {'if': {'column_id': 'Sub-Region'},'width': '25%'},                     
                                {'if': {'column_id': 'Region'},'width': '12%'},
                                {'if': {'column_id': 'Size'},'width': '12%'},
                                {'if': {'column_id': 'Updated'},'width': '25%'}],
                        tooltip_data=[{
                                  'Country': {'value': 'Click on country name to download data.', 'type': 'markdown'}
                              } for row in df.to_dict('records')],
                        cell_selectable=False)
      return data_table 

# ------------------------------------------------------------------------------
# Page Layout 
def App2():
    layout = html.Div([
        nav,
        html.Div([
          header,
          html.Div([
            search_by,
            radio_items,
            dropdown]),
        table],
        style={'margin':'100px'})
      ])
    return layout


