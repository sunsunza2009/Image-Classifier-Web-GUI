from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D , Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import categorical_crossentropy

def getModel(numClass,shape):
	model = Sequential()
	model.add(Conv2D(input_shape=shape,filters=64,kernel_size=(3,3),padding="same", activation="relu"))
	model.add(Conv2D(filters=64,kernel_size=(3,3),padding="same", activation="relu"))
	model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
	model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
	model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
	model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
	model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(Conv2D(filters=512, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(MaxPool2D(pool_size=(2,2),strides=(2,2)))
	model.add(Flatten())
	model.add(Dense(units=4096,activation="relu"))
	model.add(Dense(units=4096,activation="relu"))
	model.add(Dense(units=numClass, activation="softmax"))
	opt = Adam(lr=0.001)
	model.compile(optimizer=opt, loss=categorical_crossentropy, metrics=['accuracy'])
	return model