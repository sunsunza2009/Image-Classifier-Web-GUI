import random
import numpy as np
import cv2
from tqdm import tqdm
import os

def process(DATADIR,IMG_SIZE = 100):
	# All the categories you want your neural network to detect
	CATEGORIES = os.listdir(DATADIR)

	# The size of the images that your neural network will use
	IMG_SIZE = 100

	training_data = []

	def create_training_data():
		for category in CATEGORIES:
			path = os.path.join(DATADIR, category)
			class_num = CATEGORIES.index(category)
			for img in tqdm(os.listdir(path)):
				try :
					img_array = cv2.imread(os.path.join(path, img), cv2.IMREAD_GRAYSCALE)
					new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
					training_data.append([new_array, class_num])
				except Exception as e:
					pass

	create_training_data()

	random.shuffle(training_data)

	X = [] #features
	y = [] #labels

	for features, label in training_data:
		X.append(features)
		y.append(label)

	X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)

	# normalizing data (a pixel goes from 0 to 255)
	X = X/255.0
	return CATEGORIES, X, y
	
def proc_predict(imgPath,IMG_SIZE = 100):
	file_bytes = np.asarray(bytearray(imgPath.getbuffer()), dtype=np.uint8)
	img_array = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)
	#img_array = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
	new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
	return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)