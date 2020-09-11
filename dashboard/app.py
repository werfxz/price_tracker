import pandas as pd
import plotly.express as px
import sqlite3

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

conn = sqlite3.connect("products.db")
cur = conn.cursor()

cur.execute("""SELECT P.DATE, PR.PRODUCT_NAME, S.SELLER_NAME, P.PRICE
               FROM PRODUCTS_PRICES P
               JOIN PRODUCTS PR
                 ON P.PRODUCT_ID = PR.PRODUCT_ID
               JOIN SELLERS S
                 ON P.SELLER_ID = S.SELLER_ID
            """)
prices = cur.fetchall()
df = pd.DataFrame(prices, columns=['DATE','PRODUCT_NAME', 'SELLER_NAME', 'PRICE'])
conn.close()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,
                 external_stylesheets=[dbc.themes.BOOTSTRAP],
                 prevent_initial_callbacks=True)

app.layout = html.Div([
    html.H1(children='Price Tracker Dashboard', style={
        'textAlign': 'center'}
    ),
    html.Div(children='''
        Choose a product
    '''),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': i, 'value': i} for i in df.PRODUCT_NAME.unique()],
        placeholder="Choose a product",
        style={"width": "50%"},
        clearable=False
    ),
    dcc.Dropdown(
        id='seller-dropdown',
        options=[],
        placeholder="Choose a seller",
        style={"width": "50%"}
    ),
    dcc.Graph(id='product-price-graph')
])


@app.callback(
    [Output('seller-dropdown', 'options'),
     Output('seller-dropdown', 'value')],
    [Input('product-dropdown', 'value')]
)
def set_seller_options(selected_product):
    filtered_df = df[df.PRODUCT_NAME == selected_product].copy()
    seller_options = [{'label': i, 'value': i} for i in filtered_df.SELLER_NAME.unique()]

    return seller_options, None

@app.callback(
    Output('product-price-graph', 'figure'),
    [Input('seller-dropdown', 'options'),
     Input('seller-dropdown', 'value')],
    [State('product-dropdown', 'value')]
)
def set_seller(seller_options, selected_seller, selected_product):
    if not selected_seller:
        selected_seller = [i['value'] for i in seller_options]
    else:
        selected_seller = [selected_seller]
    
    filtered_df = df[(df.SELLER_NAME.isin(selected_seller)) &
                    (df.PRODUCT_NAME == selected_product)].copy()

    fig = px.line(filtered_df, x="DATE", y="PRICE", color="SELLER_NAME")

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)