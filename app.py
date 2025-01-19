import dash
from dash import dcc, html
import src.graph_animation as ga  
import src.graph_media as gm
import src.graph_tempo_sensor as gts  
import src.graph_tempo_all_sensors_media as gtsm  

app = dash.Dash(__name__)

app.layout = html.Div([  
    # Navbar
    html.Div(className="navbar", children=[
        html.Div(className="csv_bar", children=[]),
        html.Div(className="logo", children=[
            html.H1("AGA Integração")  
        ])
    ]),

    html.Div(className="espaco", children=[]),  # Espaço

    # Gráficos
    html.Div(className="graficos", children=[
        html.Div(className="grafico_1", children=[
            dcc.Graph(
                id="heatmap",
                figure=ga.gerar_heatmap()  # Passa o gráfico gerado pela função
            )
        ]),
        html.Div(className="grafico_2", children=[
            dcc.Graph(
                id="heatmap_media",
                figure=gm.gerar_heatmap_media()  # Passa o gráfico gerado pela função
            )
        ]),
        html.Div(className="grafico_3", children=[
            dcc.Graph(
                id="grafico_tempo_sensor",
                figure=gts.gerar_grafico_todos_sensores_tempo_30min()  # Passa o gráfico gerado pela função de tempo
            )
        ]),
        html.Div(className="grafico_4", children=[
            dcc.Graph(
                id="grafico_media_luminosidade",  # ID do novo gráfico
                figure=gtsm.gerar_grafico_media_tempo()  # Passa o gráfico de média de luminosidade
            )
        ]),
    ]),
])

if __name__ == "__main__":
    app.run_server(debug=True)
