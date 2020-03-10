from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from database import Database
from flask import current_app
import os

app = Blueprint('IMAGE', __name__)
db = Database()
MAX_UPLOAD = 64 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	id = request.form.get('id')
	_class = request.form.get('class')
	if(id != "" and id != None):
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
			db.new_image(session["id"],id,os.path.join(path, filename))
			return jsonify({"result":"Success","message":"OK"})
		else:	
			return jsonify({"result":"Fail","message":"this file is not allow"}), 400
	else:
		return jsonify({"result":"Fail","message":"id or class is require"}), 400

@app.route('/delete', methods=['GET'])
def delete():
	if 'username' not in session:
		return jsonify({"result":"Fail","message":"Login is require"}), 400
	
	id = request.args.get('id')
	if(id != "" and id != None):
		db.del_project(id,session["id"])
		return jsonify({"result":"Success","message":"OK"})
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400