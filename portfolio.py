import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

#dicionário com as informações do dropdown, em layout json, para criar subniveis.
#ESTES SÃO APENAS VALORES: SE NO LUGAR DAS LINGUAGENS, ESTIVESSEM FRUTAS, O GRÁFICO SERIA FEITO ASSIM.
dados_conceitos = {
    'java' : {
        'variaveis':8,
        'condicionais':10,
        'loops':4,
        'poo':3,
        'funções':4
    },

    'python' : {
        'variaveis':9,
        'condicionais':7,
        'loops':8,
        'poo':4,
        'funções':5
    },

    'sql' : {
        'variaveis':7,
        'condicionais':10,
        'loops':9,
        'poo':4,
        'funções':4
    },

    'golang' : {
        'variaveis':10,
        'condicionais':5,
        'loops':8,
        'poo':3,
        'funções':3
    },

    'javascript' : {
        'variaveis':8,
        'condicionais':7,
        'loops':4,
        'poo':3,
        'funções':8
    }
}
    #dicionário de cores, comum em python
    cores_map=dict(
        java ='red',
        python = 'green',
        sql = 'yellow',
        golang = 'blue',
        javascript = 'pink'
    )
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        html.H4(
            'Sebrae Maranhão'
            style={'textAlign':'center'}
        ),

        html.Div(
            dcc.Dropdown(
                id = "dropdown_linguagens",
                oprtions = [
                    {'label' : 'Java', 'value':'java'},
                    {'label' : 'Python', 'value':'python'},
                    {'label' : 'SQL', 'value':'sql'},
                    {'label' : 'GoLang', 'value':'golang'},
                    {'label' : 'JavaScript', 'value':'javascript'}
                ],
                value=['java'],
                multi=True,
                style={ 'width':'50%', 
                        'margin':'0 auto'
                        }
            )
        ),
        dcc.Graph(id='grafico_linguagem')
    ],

    style = {'width':'80%', 'margin':'0 auto'}
    
    )
    @app.callback(#uma função que vai ser chamada através de um evento.
        #esta é a saída, que será montada na figura, e os valores dessa figura estarão no dropdown.
        #Por isso, este Input esta nos colchetes
        Output('grafico_linguagem','figure'),
        [Input('dropdown_linguagens','value')]

    )

    def scarter_linguagens(linguagens_selecionadas): 
        scarter_trace = []
        #looping para trazer as linguagens
        for linguagem in linguagens_selecionadas:
            dados_linguagem = dados_conceitos[linguagem]
            #looping para trazer os itens de dados
            for conceito, conhecimento in dados_linguagem.items():
                #adicionando os dados no plano cartesiano, com marcadores
                scarter_trace.append(
                    go.Scarter(
                    x = [conceito],
                    y = [conhecimento],
                    mode = 'markers',
                    name = linguagem.title(),
                    marker={'size':15,
                            'color':cores_map[linguagem]}, 
                        showlegend=False
                    )
                )
        scarter_layout = go.layout(
            title = "Meus conhecimentos em linguagens",
            xaxis = dict(title='Conceitos', showgrid=False),
            yaxis = dict(title='Nivel de Conhecimento' showgrid=False)
        )
        
        return{'data':scarter_trace, 'layout':scarter_layout}
    
if __name__ == '__main__':
    app.run_server(debug=True)



