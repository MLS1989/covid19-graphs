import dash 
import dash_core_components as dcc 
import dash_html_components as html
import plotly.graph_objs as go  
from dash.dependencies import Input, Output, State
import pandas as pd 
from datetime import datetime



# read and mainpulate the data frame form csv
df = pd.read_csv('total-deaths-covid-19.csv')
df['Date'] = pd.to_datetime(df['Date'], format='%b %d, %Y')


tb = pd.pivot_table(df, index=['Entity','Date'], values=['Total confirmed deaths due to COVID-19 (deaths)'])
tb = tb.unstack(0)
tb.columns = tb.columns.droplevel()

#create app
app = dash.Dash(__name__)


#create list of options for multi-dropdown menu
dd_options = []
for i in tb.columns:
    dd_options.append({'label':i , 'value':i})


#create HTML layout
app.layout = html.Div([
        ### Row One - header ###
        html.Div([html.Div([html.H2('Coronavirus information dashboard')], className='col-12 col-md-9'), 
                    html.Div([html.H2('MLS-Dashboards')] , className='col-md-3 hidden-sm-down badge badge-secondary')], className='row'),
        html.Br(),
        ### Row Two- dropdowns ###
        html.Div([html.Div([
            html.Label('Select countries / regions:'),
            dcc.Dropdown(id='country-select',
                                options=dd_options, 
                                multi=True,
                                value=['United Kingdom', 'United States', 'Germany', 'Spain','Brazil'],
                                style={'padding':'10px' , 'width':'80%'}
                        ),
            html.Label('Select date range:'),
            dcc.DatePickerRange(id='date-picker',
                                min_date_allowed=datetime(2020,1,1),
                                max_date_allowed=datetime.today(),
                                start_date = datetime(2020,3,1),
                                end_date=datetime.today(),
                                style={'padding':'10px'}
                                    )], className = 'col-12 col-md-8' ),
                html.Div([html.Label('Top 5 Dropdown'), dcc.Dropdown(id='Top 5')], className = 'col-12 col-md-4')
        ], className= 'row'),
        
        html.Div([html.Div([dcc.Graph(id='my-graph',
                    figure={'data':[{'x':[1,2,3,4],'y':[2,3,4,3]}],
                            'layout':{'title':'Default title'}},)], className = 'col-12 col-lg-7'),
                html.Div([dcc.Graph(id='my-bar-chart')], className = 'col-12 col-lg-5')
                ], className = 'row'),

        
                    ], className = "container container-xl")



@app.callback(Output('my-graph', 'figure'),
            [Input('country-select', 'value'),
            Input('date-picker', 'start_date'),
            Input('date-picker', 'end_date')])
def update_graph(countries, start_date, end_date):

    start = datetime.strptime(start_date[0:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[0:10], '%Y-%m-%d' )


    data = []
    for country in countries:
        trace = go.Scatter(x=tb.loc[start_date:end_date].index, y=tb.loc[start_date:end_date][country], name=country )
        data.append(trace)

    fig = {'data':data,
            'layout':go.Layout(title='Confirmed Covid 19 deaths by country (cumulative)', 
                            yaxis={'title':'confirmed deaths'},
                            hovermode='x unified',),}
    return fig



if __name__ == "__main__":
    app.run_server()
