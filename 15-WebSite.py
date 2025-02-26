from flask import Flask, redirect, url_for, request, render_template

app = Flask(__name__)

# Crio rotas para executar blocos de comandos html
@app.route('/')
def pagina_inicial():
    return render_template('inicio.html')


@app.route('/entrar/')
def fazer_login():
    return render_template('login.html')


@app.route('/pagina403/')
def pagina403():
    return render_template('pagina403.html')


@app.route('/welcome/')
def welcome():
    return render_template('welcome.html')

@app.route('/validador/', methods=['POST', 'GET'])  # Post, envio de formulários, get, barras de busca
def validador():
    acesso_u = 'eduardo'
    acesso_s = '123'
    if request.method == 'POST':
        usuario = request.form['c_usuario']
        senha = request.form['c_senha']
        if usuario == acesso_u and senha == acesso_s:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('pagina403'))
    else:
        # Corrigido: use parênteses ao invés de colchetes
        usuario = request.args.get('c_usuario')
        senha = request.args.get('c_senha')
        if usuario == acesso_u and senha == acesso_s:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('pagina403'))

# Se o nome da minha aplicação corresponde à ela, vamos executá-la
if __name__ == '__main__':
    app.run('0.0.0.0')
