import pandas as pd
import plotly.graph_objects as go


def gerar_heatmap():
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

    # Obter os horários únicos
    horarios = sorted(df["horario"].unique())

    # Criar frames do heatmap para cada horário
    frames = []
    zmin = df["luminosidade"].min()
    zmax = df["luminosidade"].max()

    for horario in horarios:
        # Filtrar os dados para o horário atual
        df_horario = df[df["horario"] == horario]
        
        # Criar uma matriz com os valores de luminosidade
        matriz_luminosidade = []
        for linha in estrutura:
            matriz_luminosidade.append([df_horario[df_horario["sensor_n"] == sensor]["luminosidade"].values[0] for sensor in linha])

        # Adicionar o frame para o horário atual
        frames.append(
            go.Frame(
                data=[
                    go.Heatmap(
                        z=matriz_luminosidade,
                        colorscale="Viridis",
                        zmin=zmin,
                        zmax=zmax,
                        showscale=True,
                    ),
                    # go.Scatter(
                    #     x=[(j) for i in range(len(estrutura)) for j in range(len(estrutura[0]))],
                    #     y=[(i) for i in range(len(estrutura)) for j in range(len(estrutura[0]))],
                    #     mode="text",
                    #     text=[str(sensor) for linha in estrutura for sensor in linha],
                    #     textfont=dict(color="black", size=24),
                    # ),
                ],
                name=horario,
            )
        )

    # Criar o gráfico inicial (primeiro horário)
    df_inicial = df[df["horario"] == horarios[0]]
    matriz_inicial = []
    for linha in estrutura:
        matriz_inicial.append([df_inicial[df_inicial["sensor_n"] == sensor]["luminosidade"].values[0] for sensor in linha])

    # Configurar o layout
    layout = go.Layout(
        title="Heatmap de Luminosidade por Sensor",
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
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")],
                    ),
                ],
            )
        ],
        sliders=[
            dict(
                steps=[
                    dict(method="animate", args=[[horario], dict(frame=dict(duration=100, redraw=True), mode="immediate")], label=horario)
                    for horario in horarios
                ],
                active=0,
            )
        ],
    )

    # Criar a figura
    fig = go.Figure(
        data=[
            go.Heatmap(
                z=matriz_inicial,
                colorscale="Viridis",
                zmin=zmin,
                zmax=zmax,
                showscale=True,
            ),
            # go.Scatter(
            #     x=[(j) for i in range(len(estrutura)) for j in range(len(estrutura[0]))],
            #     y=[(i) for i in range(len(estrutura)) for j in range(len(estrutura[0]))],
            #     mode="text",
            #     text=[str(sensor) for linha in estrutura for sensor in linha],
            #     textfont=dict(color="black", size=24),
            # ),
        ],
        layout=layout,
        frames=frames,
    )

    # Mostrar o gráfico
    fig.show()


if __name__ == "__main__":
    gerar_heatmap()
