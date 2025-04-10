import os
import shutil
import pandas as pd

# Define a pasta de downloads
PASTA_DOWNLOADS = os.path.join(os.path.expanduser("~"), "Downloads")

# Caminho destino
DESTINO = r"G:\Meu Drive\Portfólio Camila\inmet-weather-dashboard\dados_inmet.csv"

# Procura o arquivo CSV mais recente na pasta de downloads
arquivos_csv = [f for f in os.listdir(PASTA_DOWNLOADS) if f.endswith(".csv")]
if not arquivos_csv:
    raise FileNotFoundError("Nenhum arquivo CSV encontrado na pasta de downloads.")

# Pega o arquivo mais recente
arquivo_baixado = max(
    [os.path.join(PASTA_DOWNLOADS, f) for f in arquivos_csv],
    key=os.path.getctime
)

# Move o arquivo para o destino
shutil.move(arquivo_baixado, DESTINO)
print(f"Arquivo movido para: {DESTINO}")

# Lê o arquivo com pandas
df = pd.read_csv(DESTINO, sep=";", decimal=",", encoding="utf-8")
print("\nPreview dos dados:")
print(df.head())
