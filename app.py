from flask import Flask, render_template

from Client import Client

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/creer-partie')
def creerPartie():
    liste_joueurs = [
        {"pseudo": "Annabella", "est_pret": True, "est_host":True },
        {"pseudo": "Player_Two", "est_pret": False},
        {"pseudo": "Melomane", "est_pret": True}
    ]
    return render_template('lobby.html', joueurs=liste_joueurs, code="ABCDEF")

@app.route('/connexionRoom')
def connexionRoom():
    client = Client("localhost", 888)
    client.connect()
    return render_template('temp.html')

if __name__ == '__main__':
    app.run(debug=True)