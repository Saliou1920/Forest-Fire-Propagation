import os

# https://github.com/qubvel/segmentation_models

import segmentation_models as sm
from tensorflow import keras
from tensorflow.keras.preprocessing.image import ImageDataGenerator



BACKBONE = 'resnet34'

BATCH_SIZE = 24
CLASSES = ['covid']
LR = 0.0000001
EPOCHS = 20
preprocess_input = sm.get_preprocessing(BACKBONE)


#Path
x_train_dir = "image512/images/"
y_train_dir = "image512/masks/"
x_valid_dir ="image512/val/"
y_valid_dir = "image512/valmasks/"


data_generator2 = ImageDataGenerator(preprocessing_function=preprocess_input)
data_generator = ImageDataGenerator()

#Train generators
x_generator = data_generator2.flow_from_directory(directory=x_train_dir,target_size=(512,512),batch_size=24,seed=42,class_mode=None,classes=None)
y_generator = data_generator.flow_from_directory(directory=y_train_dir,target_size=(512,512),batch_size=24,seed=42,class_mode=None,classes=None)

#Val generators
valx_generator = data_generator2.flow_from_directory(directory=x_valid_dir,target_size=(512,512),batch_size=24,seed=42,class_mode=None,classes=None)
valy_generator = data_generator.flow_from_directory(directory=y_valid_dir,target_size=(512,512),batch_size=24,seed=42,class_mode=None,classes=None)

#Method to combine the image and mask images
def combine_generator(gen1, gen2):
        while True:
            yield(next(gen1), next(gen2))

#Create new generators
generator = combine_generator(x_generator,y_generator)
valgenerator = combine_generator(valx_generator,valy_generator)

#Create model
model = sm.Unet()
model = sm.Unet('resnet34', classes=1, activation='sigmoid')
optim = keras.optimizers.Adam(LR)

#Metrics
dice_loss = sm.losses.DiceLoss()
focal_loss = sm.losses.BinaryFocalLoss()
total_loss = dice_loss + (1 * focal_loss)
metrics = [sm.metrics.IOUScore(threshold=0.5), sm.metrics.FScore(threshold=0.5)]

# compile keras model with defined optimozer, loss and metrics
model.compile(optim, total_loss, metrics)
#Fit
model.fit(generator,steps_per_epoch=3000,epochs=100,validation_data=valgenerator,validation_steps=15)
