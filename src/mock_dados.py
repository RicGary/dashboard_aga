import random
from datetime import datetime, timedelta


def main():
    QTD_SENSORES = 16

    start_time = datetime.strptime("10:00", "%H:%M")
    end_time = datetime.strptime("23:59", "%H:%M")
    delta = timedelta(minutes=1)

    # Gerar lista de horários
    HORARIOS = []
    current_time = start_time
    while current_time <= end_time:
        HORARIOS.append(current_time.strftime("%H:%M"))
        current_time += delta

    # Abrir arquivo para escrita
    with open("dados_mock.csv", "w") as f:
        f.write("sensor_n;horario;luminosidade\n")

        luminosidade_pico = 670
        luminosidade_baixo = 600

        # Iterar sobre cada horário
        for hora in HORARIOS:
            # Determinar faixa de luminosidade
            if datetime.strptime("10:00", "%H:%M") <= datetime.strptime(hora, "%H:%M") <= datetime.strptime("14:00", "%H:%M"):
                faixa_normal = (luminosidade_baixo, luminosidade_pico)
                faixa_reduzida = (luminosidade_baixo - 100, luminosidade_pico - 100)
            else:
                faixa_normal = (luminosidade_baixo - 50, luminosidade_pico - 50)
                faixa_reduzida = (luminosidade_baixo - 150, luminosidade_pico - 150)

            # Gerar valores para cada sensor
            for sensor in range(1, QTD_SENSORES + 1):
                if sensor in [1, 6, 11]:
                    luminosidade = random.randint(*faixa_reduzida)
                else:
                    luminosidade = random.randint(*faixa_normal)

                # Escrever no arquivo
                f.write(f"{sensor};{hora};{luminosidade}\n")


if __name__ == "__main__":
    main()
