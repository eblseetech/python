import dash
from dash import dcc, html
import requests
import pandas as pd
import plotly.express as px
import os

os.chdir(os.path.dirname(__file__))

app = dash.Dash(__name__)

def consultar_nomes():
    url = "https://servicodedados.ibge.gov.br/api/v2/censos/nomes/joao|maria"
    response = requests.get(url)
    dados = response.json()
    
    nomes = []
    # A resposta da API retorna um dicionário, e não uma lista
    for nome, nome_data in dados.items():
        for res in nome_data['res']:
            periodo = res['periodo']
            frequencia = res['frequencia']
            nomes.append({
                'Nome': nome,
                'Período': periodo,
                'Frequência': frequencia
            })
    df = pd.DataFrame(nomes)
    return df

def criar_grafico():
    df = consultar_nomes()  # Chamando a função dentro de criar_grafico
    fig = px.line(df, 
                  x='Período', 
                  y='Frequência', 
                  color='Nome', 
                  title='Frequência dos Nomes ao Longo dos Períodos', 
                  labels={'Período':'Período', 'Frequência':'Frequência'}
                )
    return fig

app.layout = html.Div([
    html.H1("Frequência de Nomes ao Longo dos Períodos"),
    dcc.Graph(id='grafico', figure=criar_grafico())
])

if __name__ == '__main__':
    app.run_server(debug=True)
