import cv2
from tensorflow.keras.models import load_model
from time import time
from keras import backend as K
import os
import gc

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

CATEGORIES = ["cat", "dog"]

'''def prepare(file,IMG_SIZE = 100):
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)
	

start = time()
model = load_model("CNN0.model") #your model path
image = "test.jpg" #your image path
prediction = model.predict([prepare(image)])
prediction = list(prediction[0])
print("Time: ",(time()-start))
idx = prediction.index(max(prediction))
print(CATEGORIES[idx]," ",prediction[idx])
K.clear_session()
del model
gc.collect()'''

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np

CATEGORIES = ["cat", "dog"]
testimage = "test.jpg" #your image path

img = image.load_img(testimage,target_size=(100,100))
img = np.asarray(img)
img = np.expand_dims(img, axis=0)
saved_model = load_model("CNN.model") #your model path
output = saved_model.predict(img)
output = list(output[0])
print(output)
idx = output.index(max(output))
print(CATEGORIES[idx]," ",output[idx])