import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.graph_objs as go  
from dash.dependencies import Input, Output, State
import pandas as pd 
import numpy as np  
from datetime import datetime
import json


# Try to read the dataset form the internet if not available read local csv

url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'

try:
    df = pd.read_csv(url)
    print('>>> loaded data from gitHub')
except:
    df = pd.read_csv('owid-covid-data.csv')
    print('>>> loaded data from local csv')



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


#create app
app = dash.Dash(__name__)
app.title = 'Covid19 Information Page'


#create list of options for multi-dropdown menu
dd_options = []
for i in df_deaths_cum.columns:
    dd_options.append({'label':i , 'value':i})


#text of the note to Graph2
text_g2 = """ Please note that the 'New cases' and 'New deaths' in the dropdown above relate to maximum confirmed cases or confirmed deaths recorded on a single day.
"""


#create HTML layout
app.layout = html.Div([
        ### Row One - header ###
        html.Div([html.Div([html.Img( src='assets/logo2.png')], className='col-12 col-md-4'),
                html.Div([html.H1('Coronavirus information dashboard')], className='col-12 col-md-8', style={'color': 'black'}),
                 ]
                    
            , className='row'),
        html.Div([html.Hr()]),
        html.Br(),
        ### Row Two- dropdowns and graph 1 ###
        html.Div([
            html.Div([
                html.Label('Select countries / regions:'),
                dcc.Dropdown(id='country-select',
                                options=dd_options, 
                                multi=True,
                                value=['United Kingdom', 'United States', 'Germany', 'Spain','Brazil'],
                                style={'padding':'5px',
                                    'border-radius': '3px',
                                    'box-shadow':'3px 2px 18px 0px rgba(0,0,0,0.25)',
                                    }
                        ),
                html.Br(),
                html.Label('Select the date range:   '),
                html.Br(),
                dcc.DatePickerRange(id='date-picker',
                                min_date_allowed=datetime(2020,1,1),
                                max_date_allowed=datetime.today(),
                                start_date = datetime(2020,3,1),
                                end_date=datetime.today(),
                                style={'padding':'5px',
                                    'border-radius': '3px',
                                    'box-shadow':'3px 2px 18px 0px rgba(0,0,0,0.25)',}
                            ),
                html.Br(),
                html.Br(),
                html.Div([dcc.Markdown(id='country_info',
                                     style={'padding':'5px',
                                        'border-radius': '3px',
                                        'box-shadow':'3px 2px 18px 0px rgba(0,0,0,0.25)',},
                                    children='Hover over a line on the graph to display info about the country!')],
                                    className="card"),
                
                

            ], className='col-12 col-md-4'),
                
            html.Div([
                dcc.Graph(id='my-graph',
                    figure={'data':[{'x':[1,2,3,4],'y':[1,1,1,1]}],
                            'layout':{'title':'Data unavailable'}},
                    style={}
                    )
            ], className='col-md-8'),
            
        ], className='row'),
        html.Div([html.Hr()]),
        html.Br(),

        ### Row Three - dropdown, slider and graph 2 ###
        html.Div([
            html.Div([
                html.Label('Chose data for the graph:'), dcc.Dropdown(id='drop-highest', options=dd2_options,
                                                        value='total_deaths', style={
                                                                                    'border-radius': '3px',
                                                                                    'box-shadow':'3px 2px 18px 0px rgba(0,0,0,0.25)',
                                                                                    }), 
                html.Br(),
                html.Br(),
                html.Label('Chose number of countries'), 
                dcc.Slider(
                        id='slider-highest', min=1,
                        max=10,
                        step=1,
                        value=6,
                        marks={1:'1', 5:'5',10:'10',},),
                html.Br(),
                html.Br(),
                html.Div([dcc.Markdown(children=text_g2,
                                    style={'padding':'5px',
                                        'border-radius': '3px',
                                        'box-shadow':'3px 2px 18px 0px rgba(0,0,0,0.25)',
                                        'background':'white'},
                                    className='card'
                                    )]),      
            ], className='col-md-4', style={'paddingTop':'30px'}),
            html.Div([
                dcc.Graph(id='my-bar-chart',
                        figure={'data':[{'x':['Country 1','Country 2','Country 3'],'y':[100, 80, 45]}],
                                'layout':{'title': 'Data unavailable'}
                        }
            )], className='col-md-8'),
        ], className='row'),
        html.Hr(),
        html.Br(),
        ### Row Four - dropdown date picker and graph 3 ###
        html.Div([
            html.Div([
                html.Label('Chose a country:'),
                dcc.Dropdown(id='drop-country', options=dd_options, 
                            value='United Kingdom',
                            style={
                                    'border-radius': '3px',
                                    'box-shadow':'3px 2px 18px 0px rgba(0,0,0,0.25)',
                                }),
                html.Br(),
                html.Br(),
                html.Label('Select the date range'),
                dcc.DatePickerRange(id='date-picker-2',
                                min_date_allowed=datetime(2020,1,1),
                                max_date_allowed=datetime.today(),
                                start_date = datetime(2020,3,1),
                                end_date=datetime.today(),
                                style={'padding':'5px',
                                    'border-radius': '3px',
                                    'box-shadow':'3px 2px 18px 0px rgba(0,0,0,0.25)',}),
                html.Br(),
                html.Br(),
                html.Label('Show cumulative or daily data'),
                dcc.RadioItems(id='radio', options=[
                                        {'label': 'Cumulative', 'value': 'C'},
                                        {'label': 'Daily', 'value': 'D'}
                                        ],
                                            value='D')
            ], className='col-md-4'),
            html.Div([
                html.Div([dcc.Graph(id='graph-3',
                                figure={'data':[{'x':[1,2,3,4],'y':[1,1,1,1]}],
                                    'layout':{'title':'Data unavailable'}}, )])
            ], className='col-md-8')
        ], className='row')
                ],className = "container-fluid-md container", style={
                    'background':'#E1EDF4',
                    'padding-top': '20px',
                    'padding-bottom': '20px'
                })

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
                            hovermode='closest',
                            legend_orientation="h",
                            ),}
    return fig

@app.callback(Output('my-bar-chart', 'figure'),
            [Input('drop-highest', 'value'),
            Input('slider-highest', 'value')])
def update_bar_graph(dropdown, slider):

    df_for_bar = df_highs.nlargest(slider, columns=[dropdown])
    
    data = [go.Bar(x=df_for_bar.index, y=df_for_bar[dropdown], marker={'color': df_for_bar[dropdown],
                                                                'colorscale': 'Burg'} )]
    fig = {'data':data,
            'layout':go.Layout(title='Top {} countries with highest number of {}'.format(str(slider), dropdown.replace('_',' ').capitalize()),
                                xaxis={'title':'countries'},
                                yaxis={'title':dropdown.replace('_',' ').capitalize()},
                                )}
    return fig


@app.callback(Output('country_info', 'children'),
            [Input('country-select', 'value'),
            Input('my-graph', 'hoverData')])
def country_info(countries, hoverData):
    try:
        v_index = hoverData['points'][0]['curveNumber']
        selected_country = countries[v_index]
        population = int(df[df['location']==selected_country]['population'].unique()[0])
        population_density = round(df[df['location']==selected_country]['population_density'].unique()[0],2)
        gdp_per_capita = round(df[df['location']==selected_country]['gdp_per_capita'].unique()[0],2)
        hospital_beds_per_thousand = round(df[df['location']==selected_country]['hospital_beds_per_thousand'].unique()[0],2)

        info = f"""
Selected country: **{selected_country}** \n
* Population: {population:,} \n
* Population density: {population_density:,}ppl per km square \n
* GDP per capita: {gdp_per_capita:,}$ \n
* Hospital beds: : {hospital_beds_per_thousand:,}per 1000 ppl \n"""
        return info
    except:
        info = "Hover over a line on the graph to display info about the country!"
        return info
        




@app.callback(Output('graph-3','figure'),
            [Input('drop-country','value'),
            Input('date-picker-2','start_date'),
            Input('date-picker-2','end_date'),
            Input('radio', 'value')])
def update_graph_3(country, start_date, end_date, radio):

    start = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[0:10], '%Y-%m-%d' )

    df_g3 = df[df['location']==country]
    df_g3.set_index('date', inplace=True)
    lines_cumulative = ['total_cases','total_deaths']
    lines_daily = ['new_cases', 'new_deaths']

    if radio=='C':
        lines = lines_cumulative
    else:
        lines = lines_daily

    data = [go.Bar(x=df_g3.loc[start_date:end_date].index,
                y=df_g3.loc[start_date:end_date][i], 
                name=i.replace('_',' ').capitalize()) for i in lines
        ]
    layout = go.Layout(title= f"{lines[0].replace('_',' ').capitalize()} and {lines[1].replace('_',' ').capitalize()} for {country}",
                    hovermode="x unified",
                    legend_orientation="h",
                    )
    fig = {'data':data, 'layout':layout}

    

    return fig


if __name__ == "__main__":
    app.run_server()