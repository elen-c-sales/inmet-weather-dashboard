# INMET Weather Dashboard

Projeto para coleta e visualização de dados meteorológicos da estação BRAGANÇA (A226) - INMET.

## 📊 Funcionalidades

- Coleta automatizada dos últimos 30 dias via Selenium
- Conversão de dados CSV para DataFrame
- Dashboard interativo com Plotly Dash
- Visualização de temperatura, umidade e precipitação com escalas separadas

## 📁 Estrutura

```
inmet-weather-dashboard/
├── scraping/           # Script Selenium para baixar CSV
├── dashboard/          # App Dash para visualização
├── dados_inmet.csv     # Dados salvos
└── README.md
```

## 🚀 Como executar

```bash
# Instale as dependências
pip install -r requirements.txt

# Rode o scraping (opcional)
python scraping/scraping_inmet.py

# Inicie o dashboard
python dashboard/app.py
```

## 💡 Exemplo

![screenshot](docs/dashboard_example.png)

---