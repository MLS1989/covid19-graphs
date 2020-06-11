import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.graph_objs as go  
from dash.dependencies import Input, Output, State
import pandas as pd 
import numpy as np  
from datetime import datetime


# Read the data set 
df = pd.read_csv('owid-covid-data.csv')

df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

# Create cumulative deaths by country time series tabel
df_deaths_cum = pd.pivot_table(df, index=['location','date'], values=['total_deaths'])
df_deaths_cum = df_deaths_cum.unstack(0)
df_deaths_cum.columns = df_deaths_cum.columns.droplevel()

# Create table for highest number of confirmed deaths 

df_highs = pd.pivot_table(df, index=['location'], values=
                ['total_deaths','total_cases','new_deaths','new_cases','total_cases_per_million'],
                 aggfunc=np.max)
df_highs.drop('World', inplace=True)

dd2_options = []
for i in df_highs.columns:
    dd2_options.append({'label':i.replace('_',' ').capitalize() , 'value':i})

print(dd2_options)

df_highs.to_csv('test.csv')
#create app
app = dash.Dash(__name__)


#create list of options for multi-dropdown menu
dd_options = []
for i in df_deaths_cum.columns:
    dd_options.append({'label':i , 'value':i})




#create HTML layout
app.layout = html.Div([
        ### Row One - header ###
        html.Div([html.Div([html.Img( src='assets/logo2.png')], className='col-12 col-md-3'),
                html.Div([html.H2('Coronavirus information dashboard')], className='col-12 col-md-9'),
                 ]
                    
            , className='row'),
        html.Br(),
        ### Row Two- dropdowns ###
        html.Div([
            html.Div([
                html.Label('Select countries / regions:'),
                dcc.Dropdown(id='country-select',
                                options=dd_options, 
                                multi=True,
                                value=['United Kingdom', 'United States', 'Germany', 'Spain','Brazil'],
                                style={'padding':'10px'}
                        ),
                html.Label('Select date range:'),
                dcc.DatePickerRange(id='date-picker',
                                min_date_allowed=datetime(2020,1,1),
                                max_date_allowed=datetime.today(),
                                start_date = datetime(2020,3,1),
                                end_date=datetime.today(),
                                style={'padding':'10px'}
                            ),
                html.P('Info about selected countries'),
                html.P('Country: '),
                html.P('Population:'),
                html.P('GDP per capita:'),
                html.P('Covid cases:'),
                html.P('Covid deaths:'),

            ], className='col-12 col-md-4'),
                
            html.Div([
                dcc.Graph(id='my-graph',
                    figure={'data':[{'x':[1,2,3,4],'y':[1,1,1,1]}],
                            'layout':{'title':'Data unavailable'}},
                    )
            ], className='col-md-8'),
            
        ], className='row'),
        html.Br(),
        html.Div([
            html.Div([
                html.Label('Chose data the graph:'), dcc.Dropdown(id='drop-highest', options=dd2_options,
                                                        value='total_deaths'), 
                html.Br(),
                html.Br(),
                html.Label('Chose number of countries'), dcc.Slider(id='slider-highest', min=1,
                                                                                        max=10,
                                                                                        step=1,
                                                                                        value=5,
                                                                                        marks={1:'1', 5:'5',10:'10',})
            ], className='col-md-4', style={'paddingTop':'30px'}),
            html.Div([
                dcc.Graph(id='my-bar-chart',
                        figure={'data':[{'x':['Country 1','Country 2','Country 3'],'y':[100, 80, 45]}],
                                'layout':{'title': 'Data unavailable'}
                        }
            )], className='col-md-8'),
        ], className='row')


                ], className = "container-fluid")



@app.callback(Output('my-graph', 'figure'),
            [Input('country-select', 'value'),
            Input('date-picker', 'start_date'),
            Input('date-picker', 'end_date')])
def update_graph(countries, start_date, end_date):

    start = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[0:10], '%Y-%m-%d' )

    data = []
    for country in countries:
        trace = go.Scatter(x=df_deaths_cum.loc[start_date:end_date].index, y=df_deaths_cum.loc[start_date:end_date][country], name=country )
        data.append(trace)

    fig = {'data':data,
            'layout':go.Layout(title='Confirmed Covid 19 deaths by country', 
                            yaxis={'title':'confirmed deaths'},
                            hovermode='x unified',
                            legend_orientation="h"),}
    return fig

@app.callback(Output('my-bar-chart', 'figure'),
            [Input('drop-highest', 'value'),
            Input('slider-highest', 'value')])
def update_bar_graph(dropdown, slider):

    df_for_bar = df_highs.nlargest(slider, columns=[dropdown])

    print(df_for_bar)
    
    
    data = [go.Bar(x=df_for_bar.index, y=df_for_bar[dropdown], marker={'color': df_for_bar[dropdown],
                                                                'colorscale': 'Burg'} )]
    

    fig = {'data':data,
            'layout':go.Layout(title='Top {} countries with highest number of {}'.format(str(slider), dropdown.replace('_',' ').capitalize()),
                                xaxis={'title':'countries'},
                                yaxis={'title':dropdown.replace('_',' ').capitalize()},
                            )}
    return fig
if __name__ == "__main__":
    app.run_server()