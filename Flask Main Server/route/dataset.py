from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template, send_file
from flask import current_app
import shutil, os
from database import Database

app = Blueprint('DATASET', __name__)
db = Database()

@app.route('/new', methods=['GET'])
def new():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	id = request.args.get('id')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj):
		imgpath = os.path.join(current_app.config['UPLOAD_FOLDER'],current_app.config['Image_FOLDER'],session['username'],id)
		folderpath = os.path.join(current_app.config['UPLOAD_FOLDER'],current_app.config['Dataset_FOLDER'],session['username'])
		if not os.path.exists(folderpath):
			os.makedirs(folderpath)
		if os.path.exists(imgpath):
			shutil.make_archive(os.path.join(folderpath,id), 'zip', imgpath)
			db.updateDataset(os.path.join(folderpath,id+".zip"),session["id"],id)
			return jsonify({"result":"Success","message":"OK"})
		else:
			return jsonify({"result":"Fail","message":"Image is empty"}), 400
	return jsonify({"result":"Fail","message":"id is require"}), 400

@app.route('/download', methods=['GET'])
def download():
	if 'username' not in session:
		return jsonify({"result":"Fail"}), 400
	
	id = request.args.get('id')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj):
		proj = db.get_project(session["id"],id)
		if(proj["proj_datasetPath"]):
			return send_file(proj["proj_datasetPath"], attachment_filename='dataset.zip', as_attachment=True)
		else:
			imgpath = os.path.join(current_app.config['UPLOAD_FOLDER'],current_app.config['Image_FOLDER'],session['username'],id)
			folderpath = os.path.join(current_app.config['UPLOAD_FOLDER'],current_app.config['Dataset_FOLDER'],session['username'])
			if not os.path.exists(folderpath):
				os.makedirs(folderpath)
			if os.path.exists(imgpath):
				shutil.make_archive(os.path.join(folderpath,id), 'zip', imgpath)
				db.updateDataset(os.path.join(folderpath,id+".zip"),session["id"],id)
				proj = db.get_project(session["id"],id)
				return send_file(proj["proj_datasetPath"], attachment_filename='dataset.zip', as_attachment=True)
			else:
				return jsonify({"result":"Fail","message":"Image is empty"}), 400
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400