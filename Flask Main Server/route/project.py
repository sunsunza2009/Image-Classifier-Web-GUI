from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template
from database import Database

app = Blueprint('PROJECT', __name__)
db = Database()

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
	if(id != "" and id != None):
		db.del_project(id,session["id"])
		return jsonify({"result":"Success","message":"OK"})
	else:
		return jsonify({"result":"Fail","message":"id is require"}), 400