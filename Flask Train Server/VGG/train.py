from matplotlib import pyplot as plt
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
import base64, io
from VGG.model import getModel
from VGG.preprocess import process

def getTrain(DATADIR, MODELPATH = "VGG.model", IMG_SIZE = 100):
	CATEGORIES, X, y = process(DATADIR,IMG_SIZE)
	model = getModel(len(CATEGORIES), (IMG_SIZE,IMG_SIZE,3))	
	checkpoint = ModelCheckpoint(MODELPATH, monitor='val_acc', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
	early = EarlyStopping(monitor='val_acc', min_delta=0, patience=20, verbose=1, mode='auto')
	history = model.fit_generator(steps_per_epoch=100,generator=X, validation_data=y, validation_steps=10,epochs=2,callbacks=[checkpoint,early])

	# Printing a graph showing the accuracy changes during the training phase
	plt.figure(1)
	plt.plot(history.history['acc'])
	plt.plot(history.history['val_acc'])
	plt.title('Model accuracy')
	plt.ylabel('Accuracy')
	plt.xlabel('Epoch')
	plt.legend(['train', 'validation'], loc='upper left')

	pic_IObytes = io.BytesIO()
	plt.savefig(pic_IObytes,  format='png')
	pic_IObytes.seek(0)
	pic_hash = base64.b64encode(pic_IObytes.read())
	return CATEGORIES, pic_hash