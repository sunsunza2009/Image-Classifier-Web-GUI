from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
import numpy as np

def process(DATADIR,IMG_SIZE = 100):
	trdata = ImageDataGenerator(validation_split=0.2)
	X = trdata.flow_from_directory(directory=DATADIR,target_size=(IMG_SIZE,IMG_SIZE),subset='training')
	y = trdata.flow_from_directory(directory=DATADIR, target_size=(IMG_SIZE,IMG_SIZE),subset='validation')
	return list(y.class_indices.keys()), X, y
	
def proc_predict(imgPath,IMG_SIZE = 100):
	img = image.load_img(imgPath,target_size=(IMG_SIZE,IMG_SIZE))
	img = np.asarray(img)
	img = np.expand_dims(img, axis=0)
	return img