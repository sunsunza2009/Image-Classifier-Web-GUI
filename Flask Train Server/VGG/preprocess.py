from tensorflow.keras.preprocessing.image import ImageDataGenerator

def process(DATADIR,IMG_SIZE = 100):
	trdata = ImageDataGenerator(validation_split=0.2)
	X = trdata.flow_from_directory(directory=DATADIR,target_size=(IMG_SIZE,IMG_SIZE),subset='training')
	y = trdata.flow_from_directory(directory=DATADIR, target_size=(IMG_SIZE,IMG_SIZE),subset='validation')
	return list(y.class_indices.keys()), X, y