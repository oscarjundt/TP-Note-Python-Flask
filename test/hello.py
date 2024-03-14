#imporation des bibilioteque utiliser
import sqlite3
from flask import *

Flask.secret_key = '865b1f2be442d4762ab8c67738598d7eb93e73ca3f7acf95e1c9064b56e3732f'

app = Flask(__name__)

#nom de la base de donnee sqlite
DATABASE = 'demoFlask.db'
#connection a la base de donnee
def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._database = sqlite3.connect(DATABASE)
	return db
#fermeture de la connection a la base de donnee
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
def query(sql):
	cur = get_db().execute(sql)
	rv = cur.fetchall()
	cur.close()
	return rv

#metode pour la route / qui affiche la page de login
@app.get("/")
def indexLogin():
	if "id" in session :
		return redirect("/home")
	else:
		return render_template('login.html')

#methode pour la route /home qui affiche la page de home en fonction du client connecter
@app.get("/home")
def indexHome():
	if "id"  in session :
		return render_template('home.html',id=session["id"])
	else : 
		return redirect('/')

#methode pour le
@app.get("/test")
def test():
	data = query("select id,password from login where id='"+"oscar"+"'")
	return data[0][1]

#methode pour la route post /connect qui traite les formulaire de login
# si l'utilisateur existe en BDD, rediriger vers /home et creer une session avec en valeur l'identifient
#de la personne connecter
@app.post("/connect")
def connect():
	url = "/"
	data = query("select id,password from login where id='"+request.form["username"]+"'")
	if(data is not None):
		if str(request.form["password"])==str(data[0][1]) :
			url="/home"
			session["id"]=request.form["username"]
	return redirect(url)
#methode pour la route /quit, deconnecte l'utilisateur
#supprime la session
@app.get("/quit")
def deconnect():
	url = "/"
	session.pop('id', None)
	return redirect(url)
