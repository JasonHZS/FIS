# owid-covid-data.csv:
# location
# date
# new_cases
# new_cases_per_million
#
# OxCGRT_latest_responses.csv:
# CountryName
# StartDate
# PolicyType
# PolicyValue
# Flag

import pandas as pd
import datetime

# reading data
# file_measure = r"C:/Users/hzs_J/Desktop/FIS/COVID-19/OxCGRT_latest_responses.xlsx"
file_measure1 = r"C:/Users/hzs_J/Desktop/FIS/COVID-19/数据_1.xlsx"
file_measure2 = r"C:/Users/hzs_J/Desktop/FIS/COVID-19/数据_2.xlsx"
file_cases = r"C:/Users/hzs_J/Desktop/FIS/COVID-19/owid-covid-data.xlsx"
df_case = pd.read_excel(file_cases, usecols=[2, 3, 4, 5, 11],
                        converters={u'location': str, u'date': str, u'new_cases': str, u'new_cases_per_million': str})
# df_measure = pd.read_excel(file_measure, usecols=[0, 2, 3, 4, 5, 6],
#                            converters={u'CountryName': str, u'StartDate': str, u'EndDate': str, u'PolicyType': str,
#                                        u'PolicyValue': str, u'Flag': str})
df_measure = pd.read_excel(file_measure2, usecols=[0, 2, 3, 4],
                           converters={u'CountryName': str, u'StartDate': str, u'EndDate': str, u'PolicyType': str,
                                       u'PolicyValue': str, u'Flag': str})
# data selecting and processing
# df_measure = df_measure[(df_measure['PolicyType']
#                          .isin(['C1: School closing', 'C2: Workplace closing', 'C3: Cancel public events',
#                                 'C4: Restrictions on gatherings', 'C5: Close public transport',
#                                 'C6: Stay at home requirements', 'C7: Restrictions on internal movement',
#                                 'C8: International travel controls'])) & (df_measure['Flag'].isin(['1']))
#                         & ~(df_measure['PolicyValue'].isin(['1']))
#                         & (df_measure['CountryName'].isin(['China', 'Germany', 'France', 'United Kingdom', 'Italy',
#                                                           'Spain', 'United States']))]

df_measure = df_measure.rename(columns={'StartDate': 'date', 'CountryName': 'location'})
df_measure['date'] = pd.to_datetime(df_measure['date'])
first_measure_date = df_measure.groupby(by='location')['date'].agg('min')
last_measure_date = df_measure.groupby(by='location')['date'].agg('max')
a = first_measure_date.keys()

country_sample = first_measure_date.keys()
df_case = df_case[df_case['location'].isin(country_sample)]
df_case['date'] = pd.to_datetime(df_case['date'])

# df_case['date'] = df_case['date'].str.replace('-', '')

df_result = pd.DataFrame(columns=['location', 'date', 'new_cases', 'new_cases_per_million'])
for i in range(len(country_sample)):
    first_date = first_measure_date[country_sample[i]] - datetime.timedelta(days=15)
    last_date = last_measure_date[country_sample[i]] + datetime.timedelta(days=15)
    df = df_case[(df_case['date'] >= first_date) & (df_case['date'] <= last_date)
                 & (df_case['location'].isin([country_sample[i]]))]
    df_result = df_result.append(df)

# left joining
df = pd.merge(df_result, df_measure, on=['date', 'location'], how='left')
df['date'] = df['date'].astype("str").str[0:10]

df = df.drop(columns=['EndDate'])


def ab(df):
    # return','.join(str(df.values))
    return str(df.values)


# df_policy = df[['date', 'PolicyType']].groupby(['date']).apply(lambda x: ",".join(x['PolicyType'])).reset_index()
# df = df.groupby(['location','date','new_cases','new_cases_per_million','total_cases'])['PolicyType'].apply(ab).reset_index()
nominal_data = df['PolicyType']
dummies = pd.get_dummies(nominal_data)
dummies.drop(columns=['C7: Restrictions on internal movement'], inplace=True)
result_data = pd.concat(objs=[df, dummies], axis='columns')
result_data = result_data.rename(columns={'C1: School closing': 'C1', 'C2: Workplace closing': 'C2',
                                          'C3: Cancel public events': 'C3', 'C4: Restrictions on gatherings': 'C4',
                                          'C6: Stay at home requirements': 'C6'})
# save to excel
file_out = r'C:/Users/hzs_J/Desktop/FIS/COVID-19/covid-19-result2_1.xlsx'
result_data.to_excel(file_out, index=False)

print(result_data.head())
