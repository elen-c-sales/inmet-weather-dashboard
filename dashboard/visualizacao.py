import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

# Carregar os dados
df = pd.read_csv("dados_inmet.csv", sep=';', quotechar='"')

# Padronizar os nomes das colunas
df.columns = (
    df.columns
    .str.lower()
    .str.replace('.', '', regex=False)
    .str.replace(' ', '_')
    .str.replace('(', '', regex=False)
    .str.replace(')', '', regex=False)
)

# Renomear colunas principais
df = df.rename(columns={
    'temp_ins_c': 'temperatura',
    'umi_ins_%': 'umidade',
    'chuva_mm': 'chuva'
})

# Criar coluna de data_hora
df['data_hora'] = pd.to_datetime(
    df['data'] + ' ' + df['hora_utc'].astype(str).str.zfill(4),
    format='%d/%m/%Y %H%M'
)

# Converte strings com vírgula para float
for col in ['temperatura', 'umidade', 'chuva']:
    df[col] = df[col].str.replace(',', '.').astype(float)

# Agrupar por dia para média/soma
df['data'] = df['data_hora'].dt.date
df_agg = df.groupby('data').agg({
    'temperatura': 'mean',
    'umidade': 'mean',
    'chuva': 'sum'
}).reset_index()

# Pega o último dia com dados válidos
df_agg_validos = df_agg.dropna(subset=['temperatura', 'umidade'])
ultimo_dia = df_agg_validos['data'].max()
dados_ultimo = df_agg_validos[df_agg_validos['data'] == ultimo_dia].iloc[0]

# Estilo com Open Sans
external_stylesheets = ["https://fonts.googleapis.com/css2?family=Open+Sans&display=swap"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        html.H2(f"Resumo do dia {ultimo_dia.strftime('%d/%m/%Y')}", style={'textAlign': 'center'}),

        html.Div([
            html.Div([
                html.Img(src="https://portal.inmet.gov.br/uploads/icones/temperatura_maxima.png", height="40px"),
                html.P("Temperatura (°C)", style={'margin': 0}),
                html.H4(f"{dados_ultimo['temperatura']:.1f}", style={'margin': 0}),
            ], style={'textAlign': 'center', 'width': '20%'}),

            html.Div([
                html.Img(src="https://portal.inmet.gov.br/uploads/icones/umidade_max.png", height="40px"),
                html.P("Umidade (%)", style={'margin': 0}),
                html.H4(f"{dados_ultimo['umidade']:.0f}", style={'margin': 0}),
            ], style={'textAlign': 'center', 'width': '20%'}),

            html.Div([
                html.Img(src="https://portal.inmet.gov.br/uploads/icones/precipta%C3%A7%C3%A3o.png", height="40px"),
                html.P("Chuva (mm)", style={'margin': 0}),
                html.H4(f"{dados_ultimo['chuva']:.1f}", style={'margin': 0}),
            ], style={'textAlign': 'center', 'width': '20%'}),
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'})
    ]),

    html.H1("Dados Meteorológicos - INMET (média diária)", style={'textAlign': 'center'}),

    dcc.Graph(id='grafico_inmet')
], style={'fontFamily': 'Open Sans, Arial, sans-serif', 'padding': '20px'})


@app.callback(
    Output('grafico_inmet', 'figure'),
    Input('grafico_inmet', 'id')  # Apenas para disparar a atualização uma vez
)
def atualizar_grafico(_):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_agg['data'],
        y=df_agg['temperatura'],
        name='Temperatura (°C)',
        yaxis='y1',
        line=dict(color='firebrick')
    ))

    fig.add_trace(go.Scatter(
        x=df_agg['data'],
        y=df_agg['umidade'],
        name='Umidade (%)',
        yaxis='y2',
        line=dict(color='royalblue')
    ))

    fig.add_trace(go.Bar(
        x=df_agg['data'],
        y=df_agg['chuva'],
        name='Chuva (mm)',
        yaxis='y3',
        opacity=0.5,
        marker_color='seagreen'
    ))

    fig.update_layout(
        xaxis=dict(title='Data'),
        yaxis=dict(title='Temperatura (°C)', side='left'),
        yaxis2=dict(title='Umidade (%)', overlaying='y', side='right'),
        yaxis3=dict(title='Chuva (mm)', anchor='free', overlaying='y', side='right', position=0.95),
        legend=dict(x=0, y=1),
        height=600,
        margin=dict(l=50, r=80, t=50, b=50)
    )

    return fig


if __name__ == '__main__':
    app.run(debug=True)
