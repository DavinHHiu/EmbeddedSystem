import keras
import os
import pathlib
import numpy as np
import cv2
from asgiref.sync import sync_to_async

BASEDIR = pathlib.Path(__file__).resolve().parent
model_path = os.path.join(BASEDIR, 'tomato_detection_model.h5')
model = keras.models.load_model(model_path)

labels = os.listdir(os.path.join(BASEDIR, 'tomato', 'train'))

@sync_to_async
def disease_detector(image):
    resized_image = cv2.resize(image, (256, 256))

    input_data = np.expand_dims(resized_image, axis=0)

    predictions = model.predict(input_data)

    prediction_class = np.argmax(predictions)
    return labels[prediction_class - 1]

