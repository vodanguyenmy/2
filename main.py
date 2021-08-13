from fastapi import FastAPI
#from tensorflow.keras.models import Model, load_model
import tensorflow as tf
import numpy as np
import cv2

import urllib.request

#import uvicorn
import os
import urllib.request
import random
import string
# from typing import Optional
from pydantic import BaseModel

from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.preprocessing import image
# from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications.xception import preprocess_input, decode_predictions
from tensorflow.keras.layers import Input

# Model
model = tf.keras.models.load_model("data/100_fix.h5")
class_names = ['CrdChicken', 'FluChicken', 'MarekChicken', 'NewscatleChicken', 'NormalChicken']
input_size = (224, 224, 3)
input_tensor = Input(shape=(224, 224, 3))
cmodel = Xception(input_tensor=input_tensor, weights='imagenet', include_top=True)
# Fast api
app = FastAPI()


class Image(BaseModel):
    url: str


@app.post("/api/")
async def create_item(im: Image):
    # donwload
    name = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
        string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
        string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(
        string.ascii_letters) + random.choice(string.ascii_letters) + str(random.randrange(1, 1000))
    fn = "data/img/" + name + ".jpg"
    urllib.request.urlretrieve(im.url, fn)
    # check chicken
    img = image.load_img(fn, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    name = (decode_predictions(cmodel.predict(x), top=1)[0])[0][1]
    myResult = ''
    print("name: ", name)
    if name == "hen" or name == "cock":
        mimage = cv2.imread(fn)
        mimage = cv2.resize(mimage, dsize=input_size[:2])
        mimage = mimage / 255
        mimage = np.expand_dims(mimage, axis=0)
        output = model.predict(mimage)
        class_name = class_names[np.argmax(output)]
        if class_name == "CrdChicken":
            myResult = "CRD chicken"
        elif class_name == "FluChicken":
            myResult = "Flu chicken"
        elif class_name == "MarekChicken":
            myResult = "Marek chicken"
        elif class_name == "NewscatleChicken":
            myResult = "Newscatle chicken"
        elif class_name == "NormalChicken":
            myResult = "Normal chicken"
        cv2.waitKey()
        cv2.destroyAllWindows()
    else:
        myResult = "Not chicken"
    if os.path.isfile(fn):
        os.remove(fn)
    return myResult
