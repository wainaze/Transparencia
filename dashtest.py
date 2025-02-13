from dash import Dash, dash_table, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import pandas as pd
from cbb_result import *
from transp_url import *

df = pd.read_excel('test.xlsx', sheet_name='Sheet1')

cbb_base = "https://consult.cbso.nbb.be/consult-enterprise/"
bce_base = "https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer="

#URL examples format:
#https://consult.cbso.nbb.be/consult-enterprise/0316381039
#https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer=0316381039

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = "link"
    return f'<a target="_blank" href="{link}">{text}</a>'

df['NUM'] = df['NUM'].astype(str).str.replace('.', '')

#create links to BCE and centrale des bilans 
cbb_link = cbb_base + df['NUM']
df['cbb_link'] = cbb_link

bce_link = bce_base + df['NUM']
df['bce_link'] = bce_link

df = df.astype({'cbb_link':'string'})
df = df.astype({'bce_link':'string'})
df = df.astype({'WEBSITE':'string'})
#print(df['WEBSITE'])

#use cbb_result function to check if accounts are available or not and display in cbb_result column

df['cbb_result'] = df['cbb_link'].apply(cbb_result)
df = df.astype({'cbb_result':'string'})
#print (df['cbb_result'])
#print(df)

#use transp_url function to check if there is a transparency page in a url and return the link in transp_link column

df['transp_link'] = df['WEBSITE'].map(transp_url)
df = df.astype({'transp_link':'string'})
pd.set_option('display.max_colwidth', None)
#df = df.style.format({'cbb_link': make_clickable})

#print (df)
app = Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
        ],
        #data=df.to_dict('records'),
        #editable=True,
        filter_action="native",
        sort_action="native",
        #sort_mode="multi",
        #column_selectable="single",
        #row_selectable="multi",
        #row_deletable=True,
        #selected_columns=[],
        #selected_rows=[],
        #page_action="native",
        #page_current= 0,
        #page_size= 10,
    ),
    html.Div(id='datatable-interactivity-container')
])

