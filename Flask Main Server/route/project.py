from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
from database import Database
from flask import current_app
import shutil, os

app = Blueprint('PROJECT', __name__)
db = Database()

def deleteFile(path):
	if os.path.exists(path):
		os.remove(path)
def deleteDir(path):
	if os.path.exists(path):
		shutil.rmtree(path)

@app.route('/new', methods=['GET'])
def new():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400

	name = request.args.get('name')
	type = request.args.get('type')
	if(name != "" and name != None and type != "" and type != None):
		db.new_project(name,type,session["id"])
		return jsonify({"result":"Success","message":"OK"})
	else:
		return jsonify({"result":"Fail","message":"name or type is require"}), 400

@app.route('/delete', methods=['GET'])
def delete():
	if 'username' not in session:
		return jsonify({"result":"Fail"}), 400
	
	id = request.args.get('id')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj):
		db.del_project(id,session["id"])
		path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_app.config['Image_FOLDER'], session['username'], id)
		deleteDir(path)
		path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_app.config['Dataset_FOLDER'], session['username'], id+".zip")
		deleteFile(path)
		path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_app.config['Model_FOLDER'], session['username'], id)
		deleteDir(path)
		return jsonify({"result":"Success","message":"OK"})
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400