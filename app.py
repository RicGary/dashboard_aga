import dash
import base64
from dash import dcc, html, Input, Output, callback
import src.graph_animation as ga  
import src.graph_media as gm
import src.graph_tempo_sensor as gts  
import src.graph_tempo_all_sensors_media as gtsm  

import io
import pandas as pd

app = dash.Dash(__name__)

app.layout = html.Div([  
    # Navbar
    html.Div(className="navbar", children=[
        # CSV Upload
        html.Div(className="csv_bar", children=[
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select File')
                ])
            )
        ]),

        # Logo
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
                figure={}  # Figura inicial vazia
            )
        ]),
        html.Div(className="grafico_2", children=[
            dcc.Graph(
                id="heatmap_media",
                figure={}  # Passa o gráfico gerado pela função
            )
        ]),
        html.Div(className="grafico_3", children=[
            dcc.Graph(
                id="grafico_tempo_sensor",
                figure={}  # Passa o gráfico gerado pela função de tempo
            )
        ]),
        html.Div(className="grafico_4", children=[
            dcc.Graph(
                id="grafico_media_luminosidade",  # ID do novo gráfico
                figure={}  # Passa o gráfico de média de luminosidade
            )
        ]),
    ]),
])

def parse_csv(contents):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    # Adiciona o separador correto
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep=';')
    return df  

@callback(
    Output('heatmap', 'figure'),
    Output('heatmap_media', 'figure'),
    Output('grafico_tempo_sensor', 'figure'),
    Output('grafico_media_luminosidade', 'figure'),
    Input('upload-data', 'contents')
)
def update_output(contents):
    if contents is None:
        return dash.no_update  # Não atualiza se nenhum arquivo foi enviado.

    df = parse_csv(contents)

    # background_color = "#FFF6DA"
    background_color = "white"

    gerar_heatmap = ga.gerar_heatmap(df)
    # gerar_heatmap.update_layout(
    #     paper_bgcolor=background_color,  # Cor de fundo
    #     plot_bgcolor=background_color,  # Cor da área de plotagem
    # )

    gerar_heatmap_media = gm.gerar_heatmap_media(df)
    # gerar_heatmap_media.update_layout(
    #     paper_bgcolor=background_color,  # Cor de fundo
    #     plot_bgcolor=background_color,  # Cor da área de plotagem
    # )

    gerar_grafico_todos_sensores_tempo_30min = gts.gerar_grafico_todos_sensores_tempo_30min(df)
    gerar_grafico_todos_sensores_tempo_30min.update_layout(
        paper_bgcolor=background_color,  # Cor de fundo
        # plot_bgcolor=background_color,  # Cor da área de plotagem
    )

    gerar_grafico_media_tempo = gtsm.gerar_grafico_media_tempo(df)
    gerar_grafico_media_tempo.update_layout(
        paper_bgcolor=background_color,  # Cor de fundo
        # plot_bgcolor=background_color,  # Cor da área de plotagem
    )


    return gerar_heatmap, gerar_heatmap_media, gerar_grafico_todos_sensores_tempo_30min, gerar_grafico_media_tempo
    

if __name__ == "__main__":
    app.run_server(debug=True)
