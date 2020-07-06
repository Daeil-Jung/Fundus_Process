import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

import os, datetime
import pandas as pd

tf.config.set_visible_devices([], 'GPU')
tf.random.set_seed(1234)

cur_dir = os.path.abspath(os.getcwd())
csv_data = pd.read_csv(os.path.join(cur_dir, "DBdata.csv"))

batch_size = 32
epochs = 20
IMG_HEIGHT = 448
IMG_WIDTH = 448

train_dir = "Fundus" + os.sep + "train"
test_dir = "Fundus" + os.sep + "test"

num_glaucoma_tr = len(os.listdir(os.path.join(train_dir, "Glaucoma")))
num_normal_tr = len(os.listdir(os.path.join(train_dir, "Normal")))

num_glaucoma_ts = len(os.listdir(os.path.join(test_dir, "Glaucoma")))
num_normal_ts = len(os.listdir(os.path.join(test_dir, "Normal")))

total_train = num_glaucoma_tr + num_normal_tr
total_ts = num_glaucoma_ts + num_normal_ts

train_image_generator = ImageDataGenerator(rescale=1./255, validation_split=0.2) # Generator for our training, validation data
test_image_generator = ImageDataGenerator(rescale=1./255) # Generator for our test data


train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode="categorical",
                                                           subset='training')

valid_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                           directory=train_dir,
                                                           shuffle=True,
                                                           target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                           class_mode="categorical",
                                                           subset='validation')

test_data_gen = test_image_generator.flow_from_directory(batch_size=batch_size,
                                                          directory=test_dir,
                                                          target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                          class_mode='categorical')

sample_training_images, _ = next(train_data_gen)


model = Sequential([
    Conv2D(16, 3, padding='same', activation='relu',
           input_shape=(IMG_HEIGHT, IMG_WIDTH ,3)),
    MaxPooling2D(),
    Dropout(0.1),
    Conv2D(32, 3, padding='same', activation='relu'),
    Conv2D(32, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.1),
    Conv2D(64, 3, padding='same', activation='relu'),
    Conv2D(64, 3, padding='same', activation='relu'),
    MaxPooling2D(),
    Dropout(0.1),
    Flatten(),
    Dense(1024, activation='relu'),
    Dense(2, activation="softmax"),
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy', 'binary_crossentropy'])


logdir = os.path.join("logs", datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
tensorboard_callback = tf.keras.callbacks.TensorBoard(logdir, histogram_freq=1)


history = model.fit(
    train_data_gen,
    epochs=epochs,
    validation_data=valid_data_gen,
    callbacks=[tensorboard_callback],
)

predict_value = model.predict(test_data_gen)
predict_value = tf.argmax(predict_value, axis=1)
predict_value_df = pd.DataFrame(predict_value)

train_pred = model.predict(train_data_gen)


test_files_name = []
for filepath in test_data_gen.filepaths:
    test_files_name.append(filepath.split(os.sep)[-1].split("_")[:2])


extracted_data = pd.DataFrame(test_files_name)
labels = pd.DataFrame(test_data_gen.labels)


target_col = []
for i in range(len(test_files_name)):
    try:
        target_col.append(csv_data[(csv_data["study_id"] == int(test_files_name[i][0][1:])) & (csv_data["OSOD"] == test_files_name[i][1]) & (csv_data["organization"] == "DKU")].values[0][0])
    except:
        target_col.append(0)
target_col = pd.DataFrame(target_col)


extracted_data = pd.concat([target_col, extracted_data, labels, predict_value_df], axis=1, sort=False)
extracted_data.columns = ["id", "study_id", "OSOD", "labels", "predict"]


pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)


extracted_data.to_csv("model1.csv", index=False, index_label=True)


total_rows = extracted_data.shape[0]
correct_rows = extracted_data[extracted_data["labels"] == extracted_data["predict"]]
correct_rows = correct_rows.shape[0]


print(correct_rows / total_rows)