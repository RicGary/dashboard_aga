import pandas as pd
import plotly.graph_objects as go


def gerar_grafico_todos_sensores_tempo_30min():
    # Carregar os dados do CSV
    df = pd.read_csv("dados_mock.csv", sep=";")
    
    # Verificar se o arquivo foi carregado corretamente
    if df.empty:
        print("Erro: O arquivo CSV está vazio ou não foi encontrado.")
        return

    # Filtrar os horários para mostrar apenas os de 30 em 30 minutos
    horarios_30min = [hora for hora in df["horario"].unique() if ":30" in hora or hora.endswith(":00")]
    
    # Criar uma figura
    fig = go.Figure()

    # Adicionar uma linha para cada sensor
    for sensor in sorted(df["sensor_n"].unique()):
        df_sensor = df[df["sensor_n"] == sensor]
        df_sensor = df_sensor[df_sensor["horario"].isin(horarios_30min)]  # Filtrar apenas horários de 30 em 30 minutos
        
        fig.add_trace(
            go.Scatter(
                x=df_sensor["horario"],
                y=df_sensor["luminosidade"],
                mode="lines",
                name=f"Sensor {sensor}",
                line=dict(width=2),  # Personalizar espessura da linha
            )
        )

    # Configurar o layout
    fig.update_layout(
        title="Luminosidade por Sensor ao Longo do Tempo (30 em 30 minutos)",
        xaxis=dict(
            title="Horário",
            tickangle=45,
            tickvals=horarios_30min,  # Definindo os horários de 30 em 30 minutos
            showgrid=True,
            zeroline=False,
        ),
        yaxis=dict(
            title="Luminosidade",
            showgrid=True,
            zeroline=False,
        ),
        legend=dict(
            title="Sensores",
            orientation="h",
            x=0.5,
            xanchor="center",
            y=-0.2,
        ),
    )

    # Mostrar o gráfico
    fig.show()


if __name__ == "__main__":
    gerar_grafico_todos_sensores_tempo_30min()
