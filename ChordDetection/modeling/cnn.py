"""
CNN model for feature extraction
@belom96
"""
import tensorflow as tf
import warnings
warnings.filterwarnings('ignore')
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, CSVLogger
from iterators import Batch


model = models.Sequential()
model.add(layers.Conv2D(32, 3, activation='relu', input_shape=(1, 105, 15), padding='same', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.Conv2D(32, 3, activation='relu', input_shape=(32, 105, 15),  padding='same', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.Conv2D(32, 3, activation='relu', input_shape=(32, 105, 15), padding='same', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.Conv2D(32, 3, activation='relu', input_shape=(32, 105, 15),  padding='same', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.MaxPooling2D((2, 1), data_format='channels_first'))

model.add(layers.Conv2D(64, 3, activation='relu', input_shape=(32, 52, 15), padding='valid', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.Conv2D(64, 3, activation='relu', input_shape=(64, 50, 13),  padding='valid', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.MaxPooling2D((2, 1), data_format='channels_first'))

model.add(layers.Conv2D(128, (12, 9), activation='relu', input_shape=(64, 24, 11), padding='valid', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.Conv2D(25, (1, 1), activation='linear', input_shape=(128, 13, 3), padding='valid', data_format='channels_first'))
model.add(layers.Dropout(0.3))
model.add(layers.BatchNormalization(axis=1))

model.add(layers.AveragePooling2D((13, 3), data_format='channels_first'))
model.add(layers.Flatten())
model.add(layers.Softmax())


model.compile(optimizer='adam',
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=False),
              metrics=['accuracy'])


checkpoint_dir = '/home/ubuntu/chord-detection/ChordDetection/modeling/checkpoint_1'
EPOCHS = 40
BATCH_SIZE = 500
CONTEXT_W = 7
TOTAL_FRAMES = 720000

callbacks = [
        EarlyStopping(patience=5, verbose=1),
        ReduceLROnPlateau(factor=0.1, patience=5, min_lr=0.00001, verbose=1),
        ModelCheckpoint(
            filepath=checkpoint_dir,
            verbose=1,
            save_best_only=True,
            save_weights_only=True
            ),
        CSVLogger('training_1.log')
        ]


path_to_train = '/home/ubuntu/mcgill-billboard-train/'
path_to_val = '/home/ubuntu/mcgill-billboard-val/'
path_to_test = '/home/ubuntu/mcgill-billboard-test/'

batch_obj_1 = Batch(BATCH_SIZE, CONTEXT_W, path_to_train, path_to_test, path_to_val, False, True)
batch_obj_2 = Batch(BATCH_SIZE, CONTEXT_W, path_to_train, path_to_test, path_to_val, False, True)
training_generator = batch_obj_1.train_generator()
validation_generator = batch_obj_2.val_generator()

steps_per_epoch = TOTAL_FRAMES // BATCH_SIZE

#model.load_weights(checkpoint_dir)

model.fit(
        training_generator,
        validation_data=validation_generator,
        validation_steps=100000,
        callbacks=callbacks,
        steps_per_epoch=steps_per_epoch,
        epochs=EPOCHS, verbose=True, 
        )

model.save('/home/ubuntu/chord-detection/ChordDetection/modeling/models')
