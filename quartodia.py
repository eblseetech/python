import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

#comando específico para carregar corretamente arquivos, usando o Visual Code
os.chdir(os.path.dirname(__file__))

#Inicializando o app dash, quando importar essa propriedade, sempre atentar a isso
app = dash.Dash(__name__)

#arquivo gerado no trabalho anterior, gerar.py
df = pd.read_csv('vendas.csv')

#classe para estrutura de análise de dados
class AnalisadorDeVendas:
    def __init__(self, dados):
        # Inicializa a classe com o dataframe da tabela de vendas
        self.dados = dados
        self.limpar_dados()
        
    def limpar_dados(self):
        # Limpeza e preparação dos dados para análise com as demais funções
        self.dados['data'] = pd.to_datetime(self.dados['data'], errors='coerce')  # Converte as datas
        self.dados['valor'] = self.dados['valor'].replace({',': '.'}, regex=True).astype(float)
        self.dados['mes'] = self.dados['data'].dt.month
        self.dados['ano'] = self.dados['data'].dt.year
        self.dados['dia'] = self.dados['data'].dt.day
        self.dados['dia_da_semana'] = self.dados['data'].dt.weekday
        # Remove os dados ausentes nas colunas
        self.dados.dropna(subset=['produto', 'valor'], inplace=True)

    def analise_vendas_por_Produto(self, produtosFiltrados):
        df_produto = self.dados[self.dados['produto'].isin(produtosFiltrados)]
        df_produto = df_produto.groupby(['produto'])['valor'].sum().reset_index().sort_values(by='valor', ascending=True)
        fig = px.bar(
            df_produto,
            x='produto',
            y='valor',
            title="Vendas por Produto",
            color="valor"
        )
        return fig  # Certifique-se de que é um único objeto de figura
        
# Instanciar o objeto de análise de vendas
analise = AnalisadorDeVendas(df)

# Layout do app Dash
app.layout = html.Div([
    html.H1('Análise de Vendas', style={'text-align': 'center'}),
    # Cria os filtros de seleção para o painel
    html.Div([
        html.Label('Selecione os produtos'),
        dcc.Dropdown(
            id='produto-dropdown',
            options=[{'label': produto, 'value': produto} for produto in df['produto'].unique()],
            multi=True,
            value=df['produto'].unique().tolist(),
            style={'width': '48%'}
        ),
        html.Label('Selecione as Regiões:'),
        dcc.Dropdown(
            id='regiao-dropdown',
            options=[{'label': regiao, 'value': regiao} for regiao in df['regiao'].unique()],
            multi=True,
            value=df['regiao'].unique().tolist(),
            style={'width': '48%'}
        ),
        html.Label('Selecione o Ano:'),
        dcc.Dropdown(
            id='ano-dropdown',
            options=[{'label': str(ano), 'value': ano} for ano in df['ano'].unique()],
            value=df['ano'].min(),
            style={'width': '48%'}
        ),
        html.Label('Selecione um período:'),
        dcc.DatePickerRange(
            id='data-picker-range',
            start_date=df['data'].min().date(),
            end_date=df['data'].max().date(),
            display_format='DD/MM/YY',
            style={'width': '48%'}
        ),
    ], style={'padding': '20px'}),
    # Gráficos
    html.Div([
        dcc.Graph(id='grafico-produto')
    ])
])

# Callback
@app.callback(
    Output('grafico-produto', 'figure'),
    Input('produto-dropdown', 'value'),
    Input('regiao-dropdown', 'value'),
    Input('ano-dropdown', 'value'),
    Input('data-picker-range', 'start_date'),
    Input('data-picker-range', 'end_date')
)
def upgrade_graphs(produtos, regioes, ano, start_date, end_date):
    try:
        # Converte a data para o formato correto
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Atualizar os gráficos de acordo com os filtros selecionados
        fig_produto = analise.analise_vendas_por_Produto(produtos)
        return fig_produto  # Deve retornar um único gráfico
    except Exception as e:
        # Sempre que ocorrer algum erro, mostrar a mensagem de erro e retornar um gráfico vazio
        print(f'Erro ao atualizar os gráficos: {str(e)}')
        return go.Figure()  # Retorna um gráfico vazio em caso de erro

# Rodar o app
if __name__ == '__main__':
    app.run_server(debug=True)