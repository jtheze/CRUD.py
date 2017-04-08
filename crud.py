import sqlite3
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__, template_folder="./")
app.config.from_object(__name__)


@app.route('/add', methods=['POST'])
def create():
    if(request.method == 'POST'):
        pseudo = request.form['pseudo']
        nom = request.form['nom']
        prenom = request.form['prenom']

        if((pseudo == "") and (nom == "") and (prenom == "")):
            return "You should write at least one field !"

        else:
            db = sqlite3.connect('crud.db')
            cur = db.cursor()

            cur.execute('INSERT INTO users (pseudo, nom, prenom) \
                        VALUES (?, ?, ?)', [pseudo, nom, prenom])
            db.commit()
            cur.close()
            db.close()

            return redirect(url_for('read'))

    return "Something went wrong... :-("


@app.route('/')
def read():
    db = sqlite3.connect('crud.db')
    db.row_factory = sqlite3.Row
    cur = db.cursor()

    cur.execute('SELECT id, pseudo, nom, prenom FROM users \
                ORDER BY id DESC')
    users = cur.fetchall()
    cur.close()
    db.close()

    return render_template('index.html', users=users)


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if(request.method == 'POST'):
        pseudo = request.form['pseudo']
        nom = request.form['nom']
        prenom = request.form['prenom']

        db = sqlite3.connect('crud.db')
        cur = db.cursor()

        cur.execute('UPDATE users SET pseudo = ?, nom = ?, prenom = ? \
                    WHERE id= ?', [pseudo, nom, prenom, id])
        db.commit()
        cur.close()
        db.close()

        return redirect(url_for('read'))

    return "Something went wrong... :-("


@app.route('/delete/<int:id>')
def delete(id):
    db = sqlite3.connect('crud.db')
    db.row_factory = sqlite3.Row

    cur = db.cursor()
    cur.execute('DELETE FROM users WHERE id = ?', [id])
    db.commit()
    cur.close()
    db.close()

    return redirect(url_for('read'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
# EOF Serveur
