#include <Wire.h>
#include <RTClib.h>
#include <light_CD74HC4067.h>
#include <SPI.h>
#include <SD.h>

RTC_DS1307 rtc;

// MUX: S0, S1, S2, S3 → 7,8,9,10
CD74HC4067 mux(7, 8, 9, 10);
const int signal_pin = A0;

// Cartão SD
const int PINO_CS = 4;   // Ajuste para o seu módulo
File dataFile;

byte numCanais = 16;
bool iniciou = false;

void setup() {
  Serial.begin(9600);
  Wire.begin();

  // --- RTC ----
  if (!rtc.begin()) {
    Serial.println("Erro: RTC não encontrado!");
    while (1);
  }

  if (!rtc.isrunning()) {
    Serial.println("RTC parado, ajustando pela hora da compilação...");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  pinMode(signal_pin, INPUT);

  // --- SD CARD ---
  Serial.print("Inicializando cartão SD...");
  if (!SD.begin(PINO_CS)) {
    Serial.println("Falha ao iniciar SD!");
    while (1);
  }
  Serial.println("Cartão SD OK!");

  // Cria arquivo e cabeçalho
  dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.print("timestamp;");
    for (byte ch = 0; ch < numCanais; ch++) {
      dataFile.print("C");
      dataFile.print(ch);
      if (ch < numCanais - 1) dataFile.print(";");
    }
    dataFile.println();
    dataFile.close();
  }

  Serial.println("Setup concluído!");
}

int readChannel(byte ch) {
  mux.channel(ch);
  delayMicroseconds(80);
  analogRead(signal_pin); // descarte
  return analogRead(signal_pin);
}

void loop() {
  DateTime now = rtc.now();

  // --- somente começa às 10:00 ---
  if (!iniciou) {
    if (now.hour() == 10 && now.minute() == 0 && now.second() == 0) {
      Serial.println("Iniciando medições às 10h...");
      iniciou = true;
    } else {
      Serial.print("Aguardando 10:00... agora é ");
      Serial.print(now.hour());
      Serial.print(":");
      Serial.println(now.minute());
      delay(1000);
      return;
    }
  }

  // ---- Construção do timestamp ----
  char timestamp[22];
  sprintf(timestamp, "%02d/%02d/%04d %02d:%02d:%02d",
          now.day(), now.month(), now.year(),
          now.hour(), now.minute(), now.second());

  Serial.println(timestamp);

  // --- Ler canais ---
  int valores[16];
  for (byte ch = 0; ch < numCanais; ch++) {
    valores[ch] = readChannel(ch);
    Serial.print("C");
    Serial.print(ch);
    Serial.print(":");
    Serial.print(valores[ch]);
    if (ch < numCanais - 1) Serial.print("  ");
  }
  Serial.println("\n");

  // --- Salvar no SD ---
  dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.print(timestamp);
    dataFile.print(";");
    for (byte ch = 0; ch < numCanais; ch++) {
      dataFile.print(valores[ch]);
      if (ch < numCanais - 1) dataFile.print(";");
    }
    dataFile.println();
    dataFile.close();
  } else {
    Serial.println("Erro ao abrir data.csv para escrita");
  }

  delay(300);  // ajuste para 1 minuto se quiser (60000)
}
