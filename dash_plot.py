
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

def sma_company_plotly(company):
    """
    This function creates dash app for plotting variable stats by company selected
    Input: Mysql connection and company specified
    Output: Figure object
    """
    
    df = yf.download('AAPL', 
                          start='2019-01-01', 
                          end='2021-06-12', 
                         progress=False,
    )

    df = df.reset_index()

    for i in ['Open', 'High', 'Close', 'Low']:
        df[i] = df[i].astype('float64')

    df['SMA_10'] = df['Close'].rolling(window=10).mean()
    df['SMA_50'] = df['Close'].rolling(window=50).mean()
    df['SMA_200'] = df['Close'].rolling(window=200).mean()

    #Create graph object Figure object with data
    fig = go.Figure()

    #Update layout for graph object Figure
    fig.update_layout(title_text = 'Plotly_Plot1',
                      xaxis_title = 'X_Axis',
                      yaxis_title = 'Y_Axis')

    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_10'],
                    mode='lines',
                    name='SMA_10'))

    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_50'],
                    mode='lines',
                    name='SMA_50'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA_200'],
                    mode='lines',
                    name='SMA_200'))              
    
    return fig


#Create DjangoDash applicaiton
app = Dash(name='StocksPlot')

#Configure app layout
app.layout = html.Div([
                html.Div([
                    
                    #Add dropdown for option selection
                    dcc.Input(id='company', value='DAL', type='text')],#Initial value for the dropdown
                    style={'width': '25%', 'margin':'0px auto'}),

                html.Div([                 
                    dcc.Graph(id = 'stocks_plot', 
                              animate = True, 
                              style={"backgroundColor": "#FFF0F5"})])
                        ])

#Define app input and output callbacks
@app.callback(
               Output('stocks_plot', 'figure'), #id of html component
              [Input('company', 'value')]) #id of html component
              
def display_value(company):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    #Get company plot with input value
    fig = sma_company_plotly(company)
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)