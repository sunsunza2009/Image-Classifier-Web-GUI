from flask import Blueprint, jsonify, session, request, redirect, url_for, render_template, send_file
from database import Database
from flask import current_app
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
import numpy as np
import os, requests, io
from model.CNN.preprocess import proc_predict as cnnProcess
from model.VGG.preprocess import proc_predict as vggProcess

app = Blueprint('PREDICT', __name__)
db = Database()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

model_lst = {"CNN":{"name":"Simple CNN","proc":cnnProcess},"VGG":{"name":"VGG16 Model","proc":vggProcess}}

@app.route('/predict', methods=['POST'])
def predict():
	id = request.args.get('id')
	key = request.args.get('apikey')
	file = request.files.get('file')
	proj = db.get_proj_api(key,id)

	getProc = model_lst[proj["proj_modelType"]]["proc"]
	#CATEGORIES = proj["proj_modelClass"]
	CATEGORIES = ["cat", "dog"]

	picfile = io.BytesIO()
	picfile.write(file.read())
	picfile.seek(0)
	img = getProc(picfile)
	saved_model = load_model(proj["proj_modelPath"])
	output = saved_model.predict(img)
	K.clear_session()
	del saved_model
	output = list(output[0])
	tmp = []
	for i in range(len(output)):
		tmp.append({"class":CATEGORIES[i],"probability":int(output[i]*100)})
	return jsonify(tmp)