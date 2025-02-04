from flask import Flask, request, jsonify, render_template
from flask_httpauth import HTTPTokenAuth
import os
import cups
import logging

token_flask = os.getenv('SECRET_KEY')

tokens = {
    token_flask: 'fertecnica'
}

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')
logging.basicConfig(filename='app.log', level=logging.DEBUG)

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

## Funcao para imprimir os arquivos
def print_file(filename, printer_selected, name):
    logging.debug('Iniciando impressão de arquivos')
    conn = cups.Connection()
    printers = conn.getPrinters()
    for printer in printers:
        logging.debug(conn.getPrinters())
        if printer == printer_selected:
            conn.printFile(printer, filename, name, {})
    ## teste para imprimir o arquivo
    ## defautl_printer = printers.keys()[0]
    ## conn.printFile(defautl_printer, filename, "", {})

@app.route('/')
def index():
    return render_template('upload.html')
## Rota para upload de arquivos e validacao do Token
@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    ## verifica se o token foi informado
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'token is missing'}), 401
    
    ## verifica se o arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    logging.debug('Token Validado')
    ## verifica o tipo do arquivo
    if file.filename.endswith('.pdf') or file.filename.endswith('.txt'):
        ## salvar o arquivo de acordo com o tipo
        if file.filename.endswith('.pdf'):
            file.save(os.path.join('files', file.filename))
            logging.debug('Arquivo PDF selecionado')
            print_file(os.path.join('files', file.filename), 'kyocera', 'Teste PDF')
            os.remove(os.path.join('files', file.filename))
        else:
            file.save(os.path.join('files', file.filename))
            logging.debug('Arquivo TXT selecionado')
            print_file(os.path.join('files', file.filename), 'zebra', 'Teste Etiqueta')
            os.remove(os.path.join('files', file.filename))
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'message': 'Invalid file format'}), 400

if __name__ == '__main__':
    ## execucao sem argumentos
    app.run(debug=True)
    ## execucao definindo qual host e porta vao acessar a aplicacao
    ##app.run(debug=True, host='0.0.0.0', port=5000)