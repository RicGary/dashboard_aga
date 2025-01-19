import pandas as pd
import plotly.graph_objects as go

def gerar_grafico_media_tempo():
    # Carregar os dados do CSV especificando o formato da data
    df = pd.read_csv("dados_mock.csv", sep=";", parse_dates=["horario"], dayfirst=True)
    
    # Verificar se o arquivo foi carregado corretamente
    if df.empty:
        print("Erro: O arquivo CSV está vazio ou não foi encontrado.")
        return None

    # Arredondar os horários para o intervalo de 30 minutos mais próximo
    df['horario'] = df['horario'].dt.floor('30min')
    
    # Calcular a média da luminosidade de todos os sensores para cada horário de 30 minutos
    media_tempo = df.groupby("horario")["luminosidade"].mean()

    # Criar o gráfico de linha
    fig = go.Figure(
        data=go.Scatter(
            x=media_tempo.index,
            y=media_tempo.values,
            mode="lines+markers",
            line=dict(color="blue", width=2),
            marker=dict(size=6),
        )
    )

    # Configurar o layout para exibir apenas o horário no eixo X
    fig.update_layout(
        title="Média da Luminosidade de Todos os Sensores ao Longo do Tempo (30 minutos)",
        xaxis=dict(
            title="Horário",
            tickformat="%H:%M",  # Exibir apenas o horário
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title="Média da Luminosidade",
            showgrid=True,
            zeroline=False,
        ),
    )

    return fig
