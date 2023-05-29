# Import the necessary modules
from dash import Dash, html, dcc, Input, Output, State
from dash import dash_table
import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Create a data object
df = pd.read_csv('assets/RegistrosDeScrapB1.csv')

# Add a bar plot for top values of cantidad by Numero de parte
top_values = df.groupby('Numero de parte')['Cantidad'].sum().nlargest(10).reset_index()

# Add a bar plot for top values of cantidad by Tripulacion
top_tripulacion = df.groupby('Tripulacion')['Cantidad'].sum().nlargest(10).reset_index()

# Initialize the app
app = Dash(__name__)
app.title = 'Scrap_B1'

# Define the app layout using CSS flexbox
app.layout = html.Div(
    style={'color': '#212325'},
    children=[
        html.Div( #ENCABEZADO
            style={'backgroundColor': '#2A6BAC', 'padding': '6pt 12pt', 'marginBottom': '12pt'},
            children=[ #IMAGEN
                html.Img(
                    src='assets/ford_logo.png',
                    height=120,
                    style={'display': 'block', 'margin-left': 'auto', 'margin-right': 'auto'}
                ),
                html.Div(
                    style={'color': '#C6C6C6', 'padding-top': '12pt',
                           'padding-bottom': '12pt', 'text-align': 'center',
                           'font-size': '40px', 'font-family': 'Lucida Console'},
                    children='REGISTROS DE SCRAP B1',
                ),
                html.Button('Mostrar Registros', id='toggle-button', n_clicks=0),
                html.Button('Reset Filters', id='reset-button', n_clicks=0, style={'marginLeft': '12pt'})
            ]
        ),
        html.Div( #CUERPO1
            style={'display': 'flex'},
            children=[
                html.Div(
                    id='table-container',
                    style={'backgroundColor': '#bcbbbc', 'width': '100%'},
                    children=[ #TABLA DE DATOS
                        html.Div(
                            children=[
                                dash_table.DataTable(
                                    style_table={'height': '300px', 'overflowY': 'auto'},
                                    page_size=5,
                                    style_data={
                                        'whiteSpace': 'normal',
                                        'height': 'auto',
                                        'border': '1px solid #212325',
                                        'padding': '6px',
                                        'textAlign': 'left',
                                    },
                                    style_header={
                                        'backgroundColor': '#212325',
                                        'border': '1px solid #212325',
                                        'color': '#BCBBBC',
                                        'textAlign': 'center',
                                        'fontWeight': 'bold'
                                    },
                                    data=df.to_dict('records'),
                                    columns=[{'name': i, 'id': i} for i in df.columns],
                                    style_data_conditional=[{
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(219, 228, 238)'
                                    }],
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div( #CUERPO2
            style={'display': 'flex'},
            children=[
                html.Div( #GRÁFICOS DE BARRAS
                    style={'display': 'flex', 'flexDirection': 'row', 'width': '100%'},
                    children=[
                        html.Div(
                            style={'backgroundColor': '#ffffff','width': '50%'},
                            children=[ #GRÁFICO DE BARRAS NP v QTY
                                dcc.Graph(
                                    id='top-values-barplot',
                                    figure={
                                        'data': [
                                            go.Bar(
                                                x=top_values['Numero de parte'],
                                                y=top_values['Cantidad'],
                                                marker=dict(color='#47A8E5')
                                            )
                                        ],
                                        'layout': {
                                            'title': 'Top Numero de parte Scrap',
                                            'xaxis': {'title': 'Numero de parte'},
                                            'yaxis': {'title': 'Cantidad'}
                                        }
                                    }
                                )
                            ]
                        ),
                        html.Div( # GRAFICO DE BARRAS TRIP v QTY
                            style={'backgroundColor': '#bcbbbc', 'width': '50%'},
                            children=[
                                dcc.Graph(
                                    id='top-tripulacion-barplot',
                                    figure={
                                        'data': [
                                            go.Bar(
                                                x=top_tripulacion['Cantidad'],
                                                y=top_tripulacion['Tripulacion'],
                                                orientation='h',
                                                marker=dict(color='#47A8E5'),

                                            )
                                        ],
                                        'layout': {
                                            'title': 'Top Scrap por Tripulación',
                                            'xaxis': {'title': 'Cantidad'},
                                            'yaxis': {'title': 'Tripulacion'}
                                        }
                                    }
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Callback to toggle the display of the table on button click
@app.callback(
    Output('table-container', 'style'),
    [Input('toggle-button', 'n_clicks')],
    [State('table-container', 'style')]
)
def toggle_table(n_clicks, table_style):
    if table_style is None:
        table_style = {}
    if n_clicks % 2 == 1:
        table_style['display'] = 'block'
    else:
        table_style['display'] = 'none'
    return table_style


@app.callback(
    [Output('top-values-barplot', 'figure'), Output('top-tripulacion-barplot', 'figure')],
    [Input('top-values-barplot', 'clickData'), Input('reset-button', 'n_clicks')]
)
def filter_graph(click_data, n_clicks):
    if n_clicks is None:
        n_clicks = 0

    if n_clicks % 2 == 1:
        # Reset the selection
        return (
            {
                'data': [
                    go.Bar(
                        x=top_values['Numero de parte'],
                        y=top_values['Cantidad'],
                        marker=dict(color='#47A8E5')
                    )
                ],
                'layout': {
                    'title': 'Top Numero de parte Scrap',
                    'xaxis': {'title': 'Numero de parte'},
                    'yaxis': {'title': 'Cantidad'}
                }
            },
            {
                'data': [
                    go.Bar(
                        x=top_tripulacion['Cantidad'],
                        y=top_tripulacion['Tripulacion'],
                        orientation='h',
                        marker=dict(color='#47A8E5')
                    )
                ],
                'layout': {
                    'title': 'Top Scrap por Tripulación',
                    'xaxis': {'title': 'Cantidad'},
                    'yaxis': {'title': 'Tripulacion'}
                }
            }
        )
    else:
        # Handle the bar selection
        if click_data is None:
            return dash.no_update, dash.no_update

        selected_num_parte = click_data['points'][0]['x']
        filtered_values = df[df['Numero de parte'] == selected_num_parte]
        return (
            {
                'data': [
                    go.Bar(
                        x=filtered_values['Numero de parte'],
                        y=filtered_values['Cantidad'],
                        marker=dict(color='#47A8E5')
                    )
                ],
                'layout': {
                    'title': f'Top Numero de parte Scrap: {selected_num_parte}',
                    'xaxis': {'title': 'Numero de parte'},
                    'yaxis': {'title': 'Cantidad'}
                }
            },
            {
                'data': [
                    go.Bar(
                        x=filtered_values['Cantidad'],
                        y=filtered_values['Tripulacion'],
                        orientation='h',
                        marker=dict(color='#47A8E5')
                    )
                ],
                'layout': {
                    'title': 'Top Scrap por Tripulación',
                    'xaxis': {'title': 'Cantidad'},
                    'yaxis': {'title': 'Tripulacion'}
                }
            }
        )


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

