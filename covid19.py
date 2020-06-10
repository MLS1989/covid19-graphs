
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
app = dash.Dash()

app.css.append_css({'external_url':'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css'})

#create list of options for multi-dropdown menu
dd_options = []
for i in tb.columns:
    dd_options.append({'label':i , 'value':i})


#create HTML layout
app.layout = html.Div([
        html.Div([
        html.H3('Select countries / regions:'),
        dcc.Dropdown(id='country-select',
                            options=dd_options, 
                            multi=True,
                            value=['United Kingdom', 'United States', 'Germany', 'France', 'Spain', 'Poland','Brazil'],
                            style={'paddingRight':'30px' , 'width':'80%'}
                    ),
        html.H3('Select date range:'),
        dcc.DatePickerRange(id='date-picker',
                            min_date_allowed=datetime(2020,1,1),
                            max_date_allowed=datetime.today(),
                            start_date = datetime(2020,3,1),
                            end_date=datetime.today(),
                            style={'padding':'15px'}
                                ),
        html.Div([dcc.Graph(id='my-graph',
                    figure={'data':[{'x':[1,2,3,4],'y':[2,3,4,3]}],
                            'layout':{'title':'Default title'}},)])
                    ])

])

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
