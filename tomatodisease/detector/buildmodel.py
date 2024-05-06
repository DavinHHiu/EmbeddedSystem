import os
import pathlib
import keras

BASE_DIR = pathlib.Path(__file__).resolve().parent

train_data = keras.utils.image_dataset_from_directory(
    os.path.join(BASE_DIR, 'tomato', 'train'),
    labels='inferred',
    label_mode='categorical',
    image_size=(256, 256),
    batch_size=32
)

train_data = train_data.map(lambda x, y: (x / 255.0, y))

val_data = keras.utils.image_dataset_from_directory(
    os.path.join(BASE_DIR, 'tomato', 'val'),
    labels='inferred',
    label_mode='categorical',
    image_size=(256, 256),
    batch_size=32
)

val_data = val_data.map(lambda x, y: (x / 255.0, y))

conv_base = keras.applications.DenseNet121(
    weights='imagenet',
    include_top=False,
    input_shape=(256,256,3),
    pooling='avg'
)

conv_base.trainable = False

model = keras.models.Sequential()
model.add(conv_base)
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dense(256, activation='relu'))
model.add(keras.layers.Dropout(0.35))
model.add(keras.layers.BatchNormalization())
model.add(keras.layers.Dense(120, activation='relu'))
model.add(keras.layers.Dense(10, activation='softmax'))

model.compile(optimizer=keras.optimizers.Adam(learning_rate=0.0001), loss='categorical_crossentropy', 
              metrics=['accuracy'])

history = model.fit(train_data, epochs=100, validation_data=val_data, callbacks=[keras.callbacks.EarlyStopping(patience=0)])

evaluation = model.evaluate(val_data)


print("Validation Loss:", evaluation[0])
print("Validation Accuracy:", evaluation[1])

model.save('tomato_detection_model.h5')