from keras.models import load_model
import numpy as np
import os, io
import cv2

from ml.image_crop import ImageCrop
from ml.image_resize import ImageResize

class Inferencia:

    def __init__(self):
        path =  os.path.join(os.getcwd(), "ml/recursos") 
        self.cataratas_model = load_model("{}/Cataratas.h5".format(path) )
        self.diabetes_model = load_model("{}/Diabetes.h5".format(path) )
        self.glaucoma_model = load_model("{}/Glaucoma.h5".format(path) )
        self.miopia_model = load_model("{}/Miopia.h5".format(path) )

    def request_file_to_image(self, photo):
        in_memory_file = io.BytesIO()
        photo.save(in_memory_file)
        data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
        color_image_flag = 1
        img = cv2.imdecode(data, color_image_flag)
        import datetime
        file_name = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        extension = photo.filename.split(".")
        extension = extension[1]
        file_name = "{}.{}".format(file_name, extension)
        path =  os.path.join(os.getcwd(), "uploads/") 
        cv2.imwrite("{}{}".format(path, file_name), img)
        if img.shape[0] != 224 and img.shape[1] != 224:
            img = ImageCrop(path, path, file_name).remove_black_pixels(True)
            image_width = 224
            keep_aspect_ratio = False
            quality = 100
            ImageResize(image_width, quality, path, path, file_name, keep_aspect_ratio).run()
            import matplotlib.image as mpimg
            img = mpimg.imread("{}{}".format(path, file_name))
        
        
        return img, "{}{}".format(path, file_name),  photo.filename.split(".")[0]

    def predict(self,  image_predict, model):
        result = model.predict(image_predict, verbose=0)
        result = result[:,  0]
        return round(result[0] * 100, 3)

    def diagnostico(self, image):
        image_predict = np.expand_dims(image, axis = 0)
        cataratas = self.predict(image_predict, self.cataratas_model)
        diabetes = self.predict(image_predict, self.diabetes_model)
        glaucoma = self.predict(image_predict, self.glaucoma_model)
        miopia = self.predict(image_predict, self.miopia_model)
        return cataratas, diabetes, glaucoma, miopia



