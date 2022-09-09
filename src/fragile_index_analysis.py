import pandas as pd

fsi_2021 = pd.read_excel('./data/fragile_index_data/fsi-2021.xlsx')
fsi_2020 = pd.read_excel('./data/fragile_index_data/fsi-2020.xlsx')
fsi_2019 = pd.read_excel('./data/fragile_index_data/fsi-2019.xlsx')
fsi_2018 = pd.read_excel('./data/fragile_index_data/fsi-2018.xlsx')
fsi_2017 = pd.read_excel('./data/fragile_index_data/fsi-2017.xlsx')
fsi_2016 = pd.read_excel('./data/fragile_index_data/fsi-2016.xlsx')
fsi_2015 = pd.read_excel('./data/fragile_index_data/fsi-2015.xlsx')

df = fsi_2021[fsi_2021['Country'] == 'Yemen']

country_data = {}
data = pd.read_csv('./data/countries.csv')
for country in data['country']:
    country = country.capitalize()
    temp_data =[]
    df_2021 = fsi_2021[fsi_2021['Country'] == country]
    df_2020 = fsi_2020[fsi_2020['Country'] == country]
    df_2019 = fsi_2019[fsi_2019['Country'] == country]
    df_2018 = fsi_2018[fsi_2018['Country'] == country]
    df_2017 = fsi_2017[fsi_2017['Country'] == country]
    df_2016 = fsi_2016[fsi_2016['Country'] == country]
    df_2015 = fsi_2015[fsi_2015['Country'] == country]
    temp_data.append(df_2021['Total'].values[0])
    temp_data.append(df_2020['Total'].values[0])
    temp_data.append(df_2019['Total'].values[0])
    temp_data.append(df_2018['Total'].values[0])
    temp_data.append(df_2017['Total'].values[0])
    temp_data.append(df_2016['Total'].values[0])
    temp_data.append(df_2015['Total'].values[0])

    country_data.update({country: temp_data})

print(country_data)
    







