from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template, send_file
from database import Database
from flask import current_app
import os, requests

app = Blueprint('MODEL', __name__)
db = Database()

@app.route('/request', methods=['GET'])
def req():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	raw = requests.get(current_app.config['Request_Training']+"?id="+str(session["id"])).json()
	if(raw["result"] == "Success"):
		return jsonify(raw)
	else:
		return jsonify(raw),400	

@app.route('/train', methods=['GET'])
def train():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	id = request.args.get('id')
	proj_lst = db.list_project(session["id"])
	idlst = [d['proj_id'] for d in proj_lst]
	proj = int(id) in idlst
	usr_proj = proj_lst[idlst.index(int(id))]
	if(proj and usr_proj["proj_datasetPath"]):
		files = {'file': open(usr_proj["proj_datasetPath"],'rb')}
		values = {"id":session["id"],"proj_id":id,'type': usr_proj["proj_modelType"]}
		r = requests.post(current_app.config['Start_Training'], files=files, data=values).json()
		return jsonify(r)
	else:
		return jsonify({"result":"Fail","message":"id or dataset is require"}), 400

@app.route('/list', methods=['GET'])
def list():
	raw = requests.get(current_app.config['List_model']).json()
	if(raw):
		return jsonify(raw)
	else:
		return jsonify(raw),400	

@app.route('/save', methods=['POST'])
def save():
	id = request.form.get('id')
	proj_id = request.form.get('proj_id')
	_class = request.form.get('class')
	file = request.files.get('file')
	path = os.path.join(current_app.config['UPLOAD_FOLDER'],current_app.config['Model_FOLDER'],id)
	if not os.path.exists(path):
		os.makedirs(path)
	file.save(os.path.join(path,proj_id+".model"))
	db.updateModel(os.path.join(path,proj_id+".model"),id,proj_id)
	return jsonify({"result":"Success","message":"OK"})

@app.route('/download', methods=['GET'])
def download():
	id = request.args.get('id')
	proj_lst = db.list_project(session["id"])
	idlst = [d['proj_id'] for d in proj_lst]
	proj = int(id) in idlst
	usr_proj = proj_lst[idlst.index(int(id))]
	proj = int(id) in [d['proj_id'] for d in proj_lst]
	if(proj):
		res = db.get_project(session["id"],id)
		return send_file(res["proj_modelPath"], attachment_filename=usr_proj["proj_modelType"]+'.model', as_attachment=True)
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400