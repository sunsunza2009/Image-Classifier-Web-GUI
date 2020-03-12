import json
from flask import Flask, g, render_template, session, redirect, url_for, escape, request, jsonify
from route import auth, project, image, dataset, model
from database import Database

# Create app
app = Flask(__name__)
db = Database()
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['UPLOAD_FOLDER'] = "File Storage"
app.config['Image_FOLDER'] = "User_image"
app.config['Dataset_FOLDER'] = "User_dataset"
app.config['Model_FOLDER'] = "User_model"
app.config['List_model'] = "http://127.0.0.1:3000/list"
app.config['Request_Training'] = "http://127.0.0.1:3000/"
app.config['Start_Training'] = "http://127.0.0.1:3000/data"
app.register_blueprint(auth.app)
app.register_blueprint(project.app, url_prefix="/api/private/project")
app.register_blueprint(image.app, url_prefix="/api/private/image")
app.register_blueprint(dataset.app, url_prefix="/api/private/dataset")
app.register_blueprint(model.app, url_prefix="/api/private/model")

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

@app.route("/project/<id>")
def project(id):
	if 'username' in session:
		checkuser()
		proj = db.get_project(session["id"],id)
		return render_template('process.html',sess=session,id=id,proj=proj)
	return redirect(url_for('AUTH.login'))

'''@app.errorhandler(Exception)
def handle_exception(e):
    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html"), 500'''

if __name__ == "__main__":
	print(app.url_map)
	app.run()