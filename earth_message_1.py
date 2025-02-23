import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

countries = ['Guinea', 'Iran', 'Trinidad and Tobago', 'Honduras', 'Lebanon',
             'Ethiopia', 'Niger', 'Afghanistan', 'India', 'American Samoa',
             'Cuba', 'Gabon', 'Nicaragua', 'Channel Islands', 'Martinique']

#requesting information from the website
url = 'https://www.worldometers.info/world-population/population-by-country/'
res = requests.get(url)
try:
    res.raise_for_status()
except Exception as exc:
    print('There was a problem: %s' % (exc))

#transforming said information into HTML format
html_bs4 = BeautifulSoup(res.content,'html.parser')

#obtains all the code that consitutes the table
table = html_bs4.find('table')
#obtians specifically the information related to each row, skipping over <table> and <thead>
table_rows = table.find_all('tr')

df_aux = []

for tr_h in table_rows:
    th = tr_h.find_all('th')
    heading = [i.text for i in th]

    if heading ==[]:
        break
    else:
        df_aux.append(heading)

for tr_d in table_rows:
    td = tr_d.find_all('td')
    row = [i.text for i in td]
    df_aux.append(row)

#creating the necessary data frame, which will only include country list and their population density
df = pd.DataFrame(df_aux)
df.drop(1, axis = 0, inplace = True)

df.columns = df.iloc[0]  # Set the first row as column names
df = df.drop(0).reset_index(drop=True)  # Drop the first row and reset index

df_pdens = pd.DataFrame({
    'Country (or dependency)' : df['Country (or dependency)'],
    'Density (P/Km²)' : df['Density (P/Km²)'],
})

#selecting only the rows of the countries we are interested in
length=len(df_pdens['Density (P/Km²)'])

final_aux=[]

for i in range(int(length)):
    country=str(df_pdens.iloc[i,0])
    for j in countries:
        if j==country:
            final_aux.append([df_pdens.iloc[i,0],df_pdens.iloc[i,1]])

df_final = pd.DataFrame(final_aux)
df_final.columns=['Country (or dependency)','Density (P/Km²)']
df_final['Density (P/Km²)'] = pd.to_numeric(df_final['Density (P/Km²)'], errors='coerce')
df_final = df_final.sort_values(by=['Density (P/Km²)'], ascending=False, ignore_index=True)


print(df_final)



