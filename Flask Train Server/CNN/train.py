from matplotlib import pyplot as plt
import base64, io
from CNN.model import getModel
from CNN.preprocess import process

def getTrain(DATADIR, MODELPATH = "CNN.model", IMG_SIZE = 100):
	CATEGORIES, X, y = process(DATADIR,IMG_SIZE)

	model = getModel(len(CATEGORIES), X.shape[1:])
	history = model.fit(X, y, batch_size=32, epochs=10, validation_split=0.2)

	# Saving the model
	model.save(MODELPATH)

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