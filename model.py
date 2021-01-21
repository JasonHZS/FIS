import pandas as pd
from statsmodels.formula.api import ols

file = r'C:/Users/hzs_J/Desktop/FIS/COVID-19/covid-19-result2_1.xlsx'
df = pd.read_excel(file)
df_Germany = df[df['location'] == 'Germany']
df_France = df[df['location'] == 'France']
df_Spain = df[df['location'] == 'Spain']

lm = ols('new_cases ~ C1 + C2 + C3 + C4 + C6', data=df_Germany).fit()
print(lm.summary())
