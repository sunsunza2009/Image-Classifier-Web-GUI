from flask import Flask, g, render_template, session, redirect, url_for, escape, request, jsonify
from route import auth
from database import Database

# Create app
app = Flask(__name__)
db = Database()
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.register_blueprint(auth.app)
'''app.register_blueprint(admin.app, url_prefix="/admin")
app.register_blueprint(nodeApi.app, url_prefix="/api/node")
app.register_blueprint(campus.api,url_prefix="/api/campus")
app.register_blueprint(building.api,url_prefix="/api/building")
app.register_blueprint(room.api,url_prefix="/api/room")'''

def checkuser():
	sess_user = db.getUser(session["username"])
	if(not sess_user or (sess_user and sess_user["api_key"] != session['key'])):
		session.pop('username', None)
		session.pop('key', None)
		return redirect(url_for('AUTH.login'))

@app.route("/")
def index():
	if 'username' in session:
		checkuser()
		proj = db.list_project(session["id"])
		return render_template('project.html',sess=session, proj=proj)
	return redirect(url_for('AUTH.login'))
	

'''@app.route("/settings")
def settings():
	if 'username' in session and session['permission'] == 1:
		sess_user = user.getUser(session["username"])
		if(not sess_user or (sess_user and sess_user[2] != session['permission'])):
			session.pop('username', None)
			session.pop('permission', None)
			return redirect(url_for('AUTH.login'))
		cur = get_db().cursor()
		res = cur.execute("select * from users")
		allnode = node.getAllNode()
		report = node.getRoom_report()
		return render_template("settings.html", sess=session, users=res, nodes=allnode, reports=report)
	return redirect(url_for('index'))'''


if __name__ == "__main__":
	print(app.url_map)
	app.run()