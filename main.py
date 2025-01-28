from flask import Flask, request, jsonify, render_template
import jwt
import os
import cups

app = Flask(__name__)

#chave secreta para assinatura
SECRET_KEY = 'CHAVE_SECRETA'

## Funcao para validar o Token
def validate_token(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return 'Token expired'
    except jwt.InvalidTokenError:
        return 'Invalid token'

## Funcao para imprimir os arquivos
def print_file(filename):
    conn = cups.Connection()
    printers = conn.getPrinters()
    for printer in printers:
        print(conn.getPrinters())
    ## teste para imprimir o arquivo
    defautl_printer = printers.keys()[0]
    conn.printFile(defautl_printer, filename, "", {})

@app.route('/')
def index():
    return render_template('upload.html')
## Rota para upload de arquivos e validacao do Token
@app.route('/upload', methods=['POST'])
def upload_file():
    """
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': ']token is missing'}), 401
    ## para remover o prefixo bearer
    token = token.split(' ')[1]
    decoded = validate_token(token)
    ## verifica se a decodificacao foi bem sucedida
    if not isinstance(decoded, dict):
        return jsonify({'message': decoded}), 401
    ## verifica se o arquivo foi enviado
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    """
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    
    ## verifica o tipo do arquivo
    if file.filename.endswith('.pdf') or file.filename.endswith('.txt'):
        ## salvar o arquivo de acordo com o tipo
        if file.filename.endswith('.pdf'):
            file.save(os.path.join('/path/files/pdf', file.filename))
            print_file(os.path.join('/path/files/pdf', file.filename))
        else:
            file.save(os.path.join('path/files/txt', file.filename))
            print_file(os.path.join('/path/files/txt', file.filename))
        return jsonify({'message': 'File uploaded successfully'}), 200
    else:
        return jsonify({'message': 'Invalid file format'}), 400

if __name__ == '__main__':
    ## execucao sem argumentos
    app.run(debug=True)
    ## execucao definindo qual host e porta vao acessar a aplicacao
    ##app.run(debug=True, host='0.0.0.0', port=5000)