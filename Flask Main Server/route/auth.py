from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
from database import Database

app = Blueprint('AUTH', __name__)
db = Database()

@app.route('/login', methods=['GET', 'POST'])
def login():
	if 'username' in session:
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		username = request.form['username']
		pwd = request.form['password']	
		res, usr_id, apikey = db.login(username,pwd)	
		if(res):
			session['username'] = username
			session['id'] = usr_id
			session['key'] = apikey
			return redirect(url_for('index'))
		else:
			return render_template("login.html",user=username)
	
	return render_template("login.html",user="")

@app.route('/register', methods=['GET', 'POST'])
def register():
	if 'username' in session:
		return redirect(url_for('index'))
	
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		pwd = request.form['password']
		res = db.register(username,email,pwd)	
		if(res):
			return render_template("login.html",user=username)
		else:
			return render_template("register.html",user=username)
	
	return render_template("register.html",user="")

@app.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('id', None)
	session.pop('username', None)
	session.pop('key', None)
	return redirect(url_for('index'))