from flask import Flask, escape, request, jsonify
from time import time
from concurrent.futures import ThreadPoolExecutor
import os, json, signal, sys, concurrent.futures.thread
from CNN.train import getTrain as cnnTrain
from VGG.train import getTrain as vggTrain

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

app = Flask(__name__)
app.config['DEBUG'] = True
executor = ThreadPoolExecutor(1)

model_lst = {"CNN":{"name":"Simple CNN","train":cnnTrain},"VGG":{"name":"VGG16 Model","train":vggTrain}}
lock = False
current_user = ["",0]

def exit_handler(signal, frame):
	executor._threads.clear()
	concurrent.futures.thread._threads_queues.clear()
	sys.exit(0)
signal.signal(signal.SIGINT, exit_handler)

def Training(id, proj_id, DATA, MODEL, type = "CNN"):
	global current_user, lock, model_lst
	getTrain = model_lst[type]["train"]
	CATEGORIES, pic_hash = getTrain(DATA, MODEL)
	lock = False
	current_user = ["",0]
	print(id)
	print(CATEGORIES)

@app.route('/')
def index():
	global current_user, lock
	id = request.args.get("id")
	if(id == None):
		return jsonify({"result":"Fail","message":"id is require."})
	if(time() - current_user[1] > 60 and lock == False):
		current_user[0] = id
		current_user[1] = time()
		print(current_user)
		return jsonify({"result":"Success","message":"Success, You have 60s to send data.","timeleft":60})
	if(current_user[0] == id):
		timeleft = int(60 - (time() - current_user[1]))
		return jsonify({"result":"Success","message":"Success, You have "+ str(timeleft) +"s to send data.","timeleft":timeleft})
	return jsonify({"result":"Fail","message":"Some User is currently in the training"})

@app.route('/list')	
def modelList():
	global model_lst
	tmp = []
	for i in model_lst.keys():
		tmp.append([i, model_lst[i]["name"]])
	return jsonify(tmp)

@app.route('/data')
def data():
	global current_user, lock
	id = request.args.get("id")
	type = request.args.get("type")
	if(id == None):
		return jsonify({"result":"Fail","message":"id is require."})
	if(current_user[0] == id and time() - current_user[1] < 60 and lock == False):
		lock = True
		DATA = "data"
		MODEL = "CNN.model"
		executor.submit(Training, id, 123, DATA, MODEL, type)
		return jsonify({"result":"Success","message":"Success, You data is currently in the training."})
	if(current_user[0] == id and lock):
		return jsonify({"result":"Success","message":"Success, You data is currently in the training."})
	return jsonify({"result":"Fail","message":"Some User is currently in the training"})

if __name__ == "__main__":
	app.run()