from dash import Dash, dcc, html, Input, Output
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import modules.stock_analytics
from modules.stock_analytics.base import stock_technical_analytics


def sma_company_plotly(company):
    """
    This function creates dash app for plotting variable stats by company selected
    Input: Mysql connection and company specified
    Output: Figure object
    """

    bu = stock_technical_analytics(company)

    df = bu.get_stock_history
    print(df)
    df_sma200 = bu.get_sma_200()
    print(df_sma200)
    df_sma50 = bu.get_sma_50()

    # Create graph object Figure object with data
    fig = go.Figure()

    # Update layout for graph object Figure
    fig.update_layout(title_text='Plotly_Plot1',
                      xaxis_title='X_Axis',
                      yaxis_title='Y_Axis')

    fig.add_trace(go.Scatter(x=df_sma50['Date'], y=df_sma50,
                             mode='lines',
                             name='SMA_50'))
    fig.add_trace(go.Scatter(x=df_sma200['Date'], y=df_sma200,
                             mode='lines',
                             name='SMA_200'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'],
                             mode='lines',
                             name='SMA_200'))
    return fig


# Create DjangoDash applicaiton

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(name='StocksPlot', external_stylesheets=external_stylesheets)

# Configure app layout
app.layout = html.Div([
    html.Div([

        # Add dropdown for option selection
        dcc.Input(id='company', value='AAPL', type='text')],  # Initial value for the dropdown
        style={'width': '25%', 'margin': '0px auto'}),
    # html.Div([

    #     # Add dropdown for option selection
    #     dcc.Input(id='year', value='2005', type='text')],  # Initial value for the dropdown
    #     style={'width': '25%', 'margin': '0px auto'}),
    # html.Div([
    #
    #     # Add dropdown for option selection
    #     dcc.Input(id='month', value='12', type='text')],  # Initial value for the dropdown
    #     style={'width': '25%', 'margin': '0px auto'}),
    #
    # html.Div([
    #
    #     # Add dropdown for option selection
    #     dcc.Input(id='day', value='25', type='text')],  # Initial value for the dropdown
    #     style={'width': '25%', 'margin': '0px auto'}),
    #
    # html.Div([
    #
    #     # Add dropdown for option selection
    #     dcc.Input(id='period', value='5y', type='text')],  # Initial value for the dropdown
    #     style={'width': '25%', 'margin': '0px auto'}),

    # day=dt.utcnow().strftime("%d"), timedelta=1, fullPeriod=False, period='5y', interval='1d'):

    html.Div([
        dcc.Graph(id='stocks_plot',
                  animate=True,
                  style={"backgroundColor": "#FFF0F5"})])
])


# Define app input and output callbacks
@app.callback(
    Output('stocks_plot', 'figure'),
    Input('company', 'value')
)
def display_value(company):
    """
    This function returns figure object according to value input
    Input: Value specified
    Output: Figure object
    """
    # Get company plot with input value
    fig = sma_company_plotly(company)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
