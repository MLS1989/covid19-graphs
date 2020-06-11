import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.graph_objs as go  
from dash.dependencies import Input, Output, State
import pandas as pd 
from datetime import datetime

df = pd.read_csv('owid-covid-data.csv')
print(df)
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')


df_deaths_cum = pd.pivot_table(df, index=['location','date'], values=['total_deaths'])
df_deaths_cum = df_deaths_cum.unstack(0)
df_deaths_cum.columns = df_deaths_cum.columns.droplevel()

df_deaths_cum.to_csv('test.csv')