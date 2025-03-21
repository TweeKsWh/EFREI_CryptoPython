from cryptography.fernet import Fernet
from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

# Vérifier si la clé existe déjà, sinon la générer et la sauvegarder
if os.path.exists('secret.key'):
    with open('secret.key', 'rb') as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as key_file:
        key_file.write(key)

f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:encrypted_value>', methods=['GET'])
def decrypt(encrypted_value):
    try:
        # Décrypter la valeur
        decrypted_value = f.decrypt(encrypted_value.encode())
        return jsonify({"decrypted_value": decrypted_value.decode()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
