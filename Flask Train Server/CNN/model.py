from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D

def getModel(numClass,shape):
	# Building the model
	model = Sequential()
	# 3 convolutional layers
	model.add(Conv2D(32, (3, 3), input_shape = shape))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size=(2,2)))

	model.add(Conv2D(64, (3, 3)))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size=(2,2)))

	model.add(Conv2D(64, (3, 3)))
	model.add(Activation("relu"))
	model.add(MaxPooling2D(pool_size=(2,2)))
	model.add(Dropout(0.25))

	# 2 hidden layers
	model.add(Flatten())
	model.add(Dense(128))
	model.add(Activation("relu"))

	model.add(Dense(128))
	model.add(Activation("relu"))

	# The output layer with N neurons, for N classes
	model.add(Dense(numClass))
	model.add(Activation("softmax"))

	# Compiling the model using some basic parameters
	model.compile(loss="sparse_categorical_crossentropy",
					optimizer="adam",
					metrics=["accuracy"])
	return model