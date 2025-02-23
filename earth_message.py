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



df = pd.DataFrame({
    'Country (or dependency)' : df['Country (or dependency)'],
    'Population (2024)' : df['Population (2024)'],
    'Land Area (Km²)' : df['Land Area (Km²)'],
})

df['Population (2024)'] = df['Population (2024)'].str.replace(',', '', regex=False) 
df['Land Area (Km²)'] = df['Land Area (Km²)'].str.replace(',', '', regex=False) 

df['Population (2024)'] = pd.to_numeric(df['Population (2024)'], errors='coerce')
df['Land Area (Km²)'] = pd.to_numeric(df['Land Area (Km²)'], errors='coerce')

df['Population Density']= df['Population (2024)'] / df['Land Area (Km²)']

df['Population Density'] = pd.to_numeric(df['Population Density'], errors='coerce')

# Check if there are any NaN values in 'Population Density'
print(df['Population Density'].isna().sum())  # This will show the count of NaN values

# Drop rows with NaN values if you want (optional)
df = df.dropna(subset=['Population Density'])

# Sort the DataFrame by 'Population Density' in descending order
df_sorted = df.sort_values(by='Population Density', ascending=False)


df_sorted = df.sort_values(by='Population Density')

length=len(df_sorted['Population Density'])

final_aux=[]

for i in range(int(length)):
    country=str(df_sorted.iloc[i,0])
    for j in countries:
        if j==country:
            final_aux.append([df_sorted.iloc[i,0],df_sorted.iloc[i,3]])

df_final = pd.DataFrame(final_aux)

print(df_final)

