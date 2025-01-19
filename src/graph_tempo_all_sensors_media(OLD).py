import pandas as pd
import plotly.graph_objects as go


def gerar_grafico_media_tempo():
    # Carregar os dados do CSV
    df = pd.read_csv("dados_mock.csv", sep=";")
    
    # Verificar se o arquivo foi carregado corretamente
    if df.empty:
        print("Erro: O arquivo CSV está vazio ou não foi encontrado.")
        return

    # Calcular a média da luminosidade de todos os sensores para cada horário
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

    # Configurar o layout
    fig.update_layout(
        title="Média da Luminosidade de Todos os Sensores ao Longo do Tempo",
        xaxis=dict(
            title="Horário",
            tickangle=45,
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title="Média da Luminosidade",
            showgrid=True,
            zeroline=False,
        ),
    )

    # Mostrar o gráfico
    fig.show()


if __name__ == "__main__":
    gerar_grafico_media_tempo()
