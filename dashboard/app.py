import pandas as pd
import plotly.express as px
import sqlite3

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State

conn = sqlite3.connect("../products.db")
cur = conn.cursor()

cur.execute("""SELECT P.DATE_TIME, PR.PRODUCT_NAME, S.SELLER_NAME, P.PRICE
               FROM PRODUCTS_PRICES P
               JOIN PRODUCTS PR
                 ON P.PRODUCT_ID = PR.PRODUCT_ID
               JOIN SELLERS S
                 ON P.SELLER_ID = S.SELLER_ID
            """)
prices = cur.fetchall()
df = pd.DataFrame(prices, columns=['DATE','PRODUCT_NAME', 'SELLER_NAME', 'PRICE'])
conn.close()

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    prevent_initial_callbacks=True
)
server = app.server

#https://dash-gallery.plotly.host/Portal/
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(
                            className="logo", src=app.get_asset_url("dash-logo-new.png")
                        ),
                        html.H2("DASH - PRICE TRACKER APP"),
                        html.P(
                            """Select different products using the product picker and select
                            different seller for specific price"""
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for locations on map
                                        dcc.Dropdown(
                                            id="product-dropdown", 
                                            options=[                               
                                                {"label": i, "value": i}
                                                for i in df.PRODUCT_NAME.unique()
                                            ],
                                            placeholder="Select a product",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times
                                        dcc.Dropdown(
                                            id="seller-dropdown",
                                            options=[],
                                            placeholder="Select a seller",
                                        )
                                    ],
                                ),
                            ],
                        ),
                        #html.P(id="total-rides"),
                        #html.P(id="total-rides-selection"),
                        #html.P(id="date-value"),
                        dcc.Markdown(
                            children=[
                                "Source: [Github](https://github.com/werfxz/price_tracker)"
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        html.Div(
                            className="price-graph",
                            children=[
                                dcc.Graph(id='product-price-graph')
                            ]
                        )
                    ],
                ),
            ],
        )
    ]
)


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

    fig = px.line(filtered_df,
                  x="DATE", y="PRICE",
                  color="SELLER_NAME", line_shape='spline',
                  template='plotly_dark',
                  height=600)

    fig.update_layout(transition_duration=500)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)