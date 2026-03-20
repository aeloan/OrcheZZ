from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/creer-partie')
def creerPartie():
    return render_template('lobby.html', code="ABCDEF")

if __name__ == '__main__':
    app.run(debug=True)