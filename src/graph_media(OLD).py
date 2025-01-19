import pandas as pd
import plotly.graph_objects as go


def gerar_heatmap_media():
    # Carregar os dados do CSV
    df = pd.read_csv("dados_mock.csv", sep=";")
    
    # Verificar se o arquivo foi carregado corretamente
    if df.empty:
        print("Erro: O arquivo CSV está vazio ou não foi encontrado.")
        return

    # Criar estrutura dos sensores
    sensores_por_linha = 4
    QTD_SENSORES = 16
    estrutura = [list(range(i, i + sensores_por_linha)) for i in range(1, QTD_SENSORES + 1, sensores_por_linha)]

    # Calcular a média da luminosidade para cada sensor
    medias_luminosidade = df.groupby("sensor_n")["luminosidade"].mean()

    # Criar uma matriz com as médias para o heatmap
    matriz_media = []
    for linha in estrutura:
        matriz_media.append([medias_luminosidade[sensor] for sensor in linha])

    # Criar o heatmap
    fig = go.Figure(
        data=[
            go.Heatmap(
                z=matriz_media,
                colorscale="Viridis",
                zmin=medias_luminosidade.min(),
                zmax=medias_luminosidade.max(),
                showscale=True,
            ),
            go.Scatter(
                x=[(j) for i in range(len(estrutura)) for j in range(len(estrutura[0]))],
                y=[(i) for i in range(len(estrutura)) for j in range(len(estrutura[0]))],
                mode="text",
                text=[str(sensor) for linha in estrutura for sensor in linha],
                textfont=dict(color="black", size=24),
            ),
        ]
    )

    # Configurar o layout
    fig.update_layout(
        title="Heatmap de Média de Luminosidade por Sensor",
        xaxis=dict(
            title="Colunas",
            tickvals=[0.5, 1.5, 2.5, 3.5],
            ticktext=["1", "2", "3", "4"],
            scaleanchor="y",  # Escalas iguais para tornar o gráfico quadrado
        ),
        yaxis=dict(
            title="Linhas",
            tickvals=[0.5, 1.5, 2.5, 3.5],
            ticktext=["1", "2", "3", "4"],
        ),
    )

    # Mostrar o gráfico
    fig.show()


if __name__ == "__main__":
    gerar_heatmap_media()
