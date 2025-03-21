from cryptography.fernet import Fernet
from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# Clé de cryptage (dans un vrai scénario, stockez cette clé en sécurité)
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/', methods=['POST'])
def decrypt():
    data = request.get_json()
    encrypted_value = data.get('value')

    if not encrypted_value:
        return jsonify({"error": "No value provided"}), 400

    try:
        # Décrypter la valeur
        decrypted_value = f.decrypt(encrypted_value.encode())
        return jsonify({"decrypted_value": decrypted_value.decode()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
