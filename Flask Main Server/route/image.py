from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template, send_file
from werkzeug.utils import secure_filename
from database import Database
from flask import current_app
import os

app = Blueprint('IMAGE', __name__)
db = Database()
MAX_UPLOAD = 64 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'jpe', 'bmp', 'tiff', 'tif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	id = request.form.get('id')
	_class = request.form.get('class')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj):
		file = request.files.get('file')
		if file == None:
			return jsonify({"result":"Fail","message":"file is require"}), 400
		file_raw = file.read()
		if len(file_raw) > MAX_UPLOAD:
			return jsonify({"result":"Fail","message":"file size is too large"}), 413
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename.split("/")[-1])
			path = os.path.join(current_app.config['UPLOAD_FOLDER'],current_app.config['Image_FOLDER'],session['username'],id,_class)
			if not os.path.exists(path):
				os.makedirs(path)
			file.seek(0)
			file.save(os.path.join(path, filename))
			imgid = db.new_image(session["id"],id,os.path.join(path, filename))
			return jsonify({"result":"Success","message":"OK","id":imgid})
		else:	
			return jsonify({"result":"Fail","message":"this file is not allow"}), 400
	else:
		return jsonify({"result":"Fail","message":"id or class is require"}), 400

@app.route('/rename', methods=['GET'])
def rename():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	id = request.args.get('id')
	_class = request.args.get('class')
	_oldclass = request.args.get('oldclass')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj):
		path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_app.config['Image_FOLDER'], session['username'], id)
		if os.path.exists(os.path.join(path, _oldclass)) and not os.path.exists(os.path.join(path, _class)):
			os.rename(os.path.join(path, _oldclass), os.path.join(path, _class))
			db.update_Class(_oldclass,_class,session["id"],id)
			return jsonify({"result":"Success","message":"OK"})
		else:
			return jsonify({"result":"Fail","message":"This class is not exit or it already exit"}), 400
	return jsonify({"result":"Fail","message":"id or class is require"}), 400

@app.route('/delete', methods=['GET'])
def delete():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	
	id = request.args.get('id')
	imgid = request.args.get('imgid')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj and imgid != "" and imgid != None):
		res = db.get_image(imgid,session["id"],id)
		db.del_image(imgid,session["id"],id)
		if os.path.exists(res["img_path"]):
			os.remove(res["img_path"])
		return jsonify({"result":"Success","message":"OK"})
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400

@app.route('/list', methods=['GET'])
def list():
	id = request.args.get('id')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj):
		img_lst = db.list_image(session["id"],id)
		tmp = []
		for i in img_lst:
			name = os.path.split(i["img_path"])[1]
			pathSplit = i["img_path"].split(os.sep)[-2]+"/"+name
			url = url_for("IMAGE.view",id=id,imgid=i["img_id"])
			tmp.append({"id":i["img_id"],"name":name,"webkitRelativePath":pathSplit,"url":url})
		return jsonify({"result":"Success","message":"OK","files":tmp})
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400

@app.route('/view', methods=['GET'])
def view():
	id = request.args.get('id')
	imgid = request.args.get('imgid')
	proj = int(id) in [d['proj_id'] for d in db.list_project(session["id"])]
	if(proj and imgid != "" and imgid != None):
		res = db.get_image(imgid,session["id"],id)
		return send_file(res["img_path"])
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400