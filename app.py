from flask import Flask, request, render_template, session, redirect, send_file
import numpy as np
import pandas as pd
from cbb_result import *
from transp_url import *
from io import BytesIO


app = Flask(__name__)

df = pd.read_excel('transparencia.xlsx', sheet_name='Sheet1')

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

df_short= df.drop(['WEBSITE', 'bce_link', 'Autorite', 'TYPE', 'MANDATS', 'UNITES'], axis=1)

#print (df)

@app.route('/')
def html_table():
    return render_template('index.html',  tables=[df_short.to_html( table_id = 'table', justify = "left", classes='table table-striped', header="true", render_links="True", escape="False")])


@app.route("/getfile")
def getPlotCSV():
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    output.seek(0)
    return send_file(output, download_name='transparencia.xlsx', as_attachment=True)

server = app.server

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)



    