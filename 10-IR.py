def calculadora_ir(salario_bruto):

    #tabela de alíquotas e faixas do imposto de renda
    tabela_ir = [
        {
            "faixa":(0,1903.98),
            "aliquota":0,
            "deducao":0
        },
        {
            "faixa":(1903.99,2826.65),
            "aliquota":7.5,
            "deducao":142
        },
        {
            "faixa":(2826.66,3751.05),
            "aliquota":15,
            "deducao":354
        },
        {
            "faixa":(3751.06,4664.68),
            "aliquota":22.5,
            "deducao":636
        },
        {
            "faixa":(4664.69,float("inf")),
            "aliquota":27.5,
            "deducao":869
        }
    ]

# calculando o imposto de renda

    imposto = 0
    for faixa in tabela_ir:
        if salario_bruto > faixa['faixa'][0] and salario_bruto <= faixa['faixa'][1]:
            resultado = (salario_bruto * faixa['aliquota']) / 100 - faixa['deducao']
            break
    return resultado

#testando nossa função de cálculo de imposto de renda

salario_bruto = float(input("Informe o seu salário Bruto: "))
resultado_final = calculadora_ir(salario_bruto)
salarioLiquido = salario_bruto - resultado_final

print(f'Seu salário bruto é {salario_bruto:.2f}')
print(f'Seu imposto devido é R$ {resultado_final:.2f}')
print(f'Seu salário Líquido, R$ {salarioLiquido:.2f}')