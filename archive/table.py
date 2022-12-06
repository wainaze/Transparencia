import pandas as pd
from cbb_result import *
from transp_url import *

df = pd.read_excel('test.xlsx', sheet_name='Sheet1')

cbb_base = "https://consult.cbso.nbb.be/consult-enterprise/"
bce_base = "https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer="

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    text = "link"
    return f'<a target="_blank" href="{link}">{text}</a>'

#URL examples format:
#https://consult.cbso.nbb.be/consult-enterprise/0316381039
#https://kbopub.economie.fgov.be/kbopub/zoeknummerform.html?nummer=0316381039

df['NUM'] = df['NUM'].astype(str).str.replace('.', '')

#create links to BCE and centrale des bilans 
cbb_link = cbb_base + df['NUM']
df['cbb_link'] = cbb_link
df['cbb_link_shortcut'] = make_clickable(cbb_link)

bce_link = bce_base + df['NUM']
df['bce_link'] = bce_link
df['cbb_link_shortcut'] = make_clickable(cbb_link)

df = df.astype({'cbb_link':'string'})
df = df.astype({'bce_link':'string'})
#df = df.astype({'WEBSITE':'string'})
#print(df['WEBSITE'])

#use cbb_result function to check if accounts are available or not and display in cbb_result column

df['cbb_result'] = df['cbb_link'].apply(cbb_result)
df = df.astype({'cbb_result':'string'})
print (df['cbb_result'])
#print(df)

#use transp_url function to check if there is a transparency page in a url and return the link in transp_link column

df['transp_link'] = df['WEBSITE'].map(transp_url)
df = df.astype({'transp_link':'string'})
pd.set_option('display.max_colwidth', None)
print (df['transp_link'])
print(df['link_shortcut'])