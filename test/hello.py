#imporation des bibilioteque utiliser
import sqlite3
from pathlib import Path
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

def init_db():
	if not Path(DATABASE).exists():
		with app.app_context():
			db = get_db()
			with app.open_resource('script.sql', mode='r') as f:
				db.cursor().executescript(f.read())
			db.commit()
init_db()
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
def insert(sql):
	cur = get_db().execute(sql)
	get_db().commit()
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
	data = query("select id,username,password from login where username='"+request.form["username"]+"'")
	if(data is not None):
		if str(request.form["password"])==str(data[0][2]) :
			url="/home"
			session["username"]=request.form["username"]
			session["id"] = data[0][0]
	return redirect(url)
#methode pour la route /quit, deconnecte l'utilisateur
#supprime la session
@app.get("/quit")
def deconnect():
	url = "/"
	session.pop('username', None)
	session.pop('id', None)
	return redirect(url)

#methode pour la route /home/list
#cette methode recupere les iframe en BDD et les revoit a la vue liste.html
@app.get("/home/list")
def index_liste():
	if "id" in session :
		data = query("select iframe.id,title,url from iframe join login on iframe.idLogin=login.id where username='"+session["username"]+"'")
		return render_template("liste.html",lists=data)
	else:
		abort(403)
#methode pour la route /home/video/{id}
#methode qui recupere un iframe en fonction de sont identifiant
@app.get("/home/video/<id>")
def index_iframe(id):
	if "id" in session :
		data = query("select title,url from iframe join login on iframe.idLogin=login.id where username='"+session["username"]+"' and iframe.id="+id)
		return  render_template("iframe.html",iframe=data)
	else:
		abort(403)
#methode pour la route /home/ajout
#affiche la vue du formulaire pour ajouter un iframe
@app.get("/home/ajout")
def index_ajout():
	if "id" in session :
		return  render_template("ajout.html")
	else:
		redirect("/")
#ajout d'un iframe methode post
@app.post("/home/ajout")
def index_ajout_iframe():
	if "id" in session :
		if(request.form["title"] and request.form["url"]):
			data = insert("insert into iframe (title,url,idLogin) values ('"+request.form["title"]+"','"+request.form["url"]+"',"+str(session['id'])+")")
			return redirect('/home/list')
	else:
		abort(403)

#suppression d'un iframe en fonction de sont identifiant
@app.get("/home/supp/<id>")
def supp_iframe(id):
	if "id" in session :
			data = insert("delete from iframe where id="+id)
			return redirect('/home/list')
	else:
		abort(403)