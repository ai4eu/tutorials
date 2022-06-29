import grpc
from concurrent import futures
import time
import news_classifier_pb2
import news_classifier_pb2_grpc
import os
import numpy as np
import tensorflow.keras
from tensorflow.keras import layers
from tensorflow.keras import callbacks
from tensorflow.keras.datasets import reuters
from tensorflow.keras.preprocessing import sequence


port = 8061
shared_folder = os.getenv("SHARED_FOLDER_PATH")
rev_topic_map = {'copper': 6, 'livestock': 28, 'gold': 25, 'money-fx': 19, 'ipi': 30, 'trade': 11, 'cocoa': 0, 'iron-steel': 31, 'reserves': 12, 'tin': 26, 'zinc': 37, 'jobs': 34, 'ship': 13, 'cotton': 14, 'alum': 23, 'strategic-metal': 27, 'lead': 45, 'housing': 7, 'meal-feed': 22, 'gnp': 21, 'sugar': 10, 'rubber': 32, 'dlr': 40, 'veg-oil': 2, 'interest': 20, 'crude': 16, 'coffee': 9, 'wheat': 5, 'carcass': 15, 'lei': 35, 'gas': 41, 'nat-gas': 17, 'oilseed': 24, 'orange': 38, 'heat': 33, 'wpi': 43, 'silver': 42, 'cpi': 18, 'earn': 3, 'bop': 36, 'money-supply': 8, 'hog': 44, 'acq': 4, 'pet-chem': 39, 'grain': 1, 'retail': 29}
topic_map = dict([(value, key) for key, value in rev_topic_map.items()])
word_index = reuters.get_word_index()
tensorboard_callback = callbacks.TensorBoard(log_dir=shared_folder)



class NewsClassifier(news_classifier_pb2_grpc.NewsClassifierServicer):

    def __init__(self):
        self.model = tensorflow.keras.Sequential([
            layers.Dense(64, activation='relu'),
            layers.Dense(64, activation='relu'),
            layers.Dense(46, activation='softmax')
        ])

        self.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])

    def startTraining(self, request, context):
        print(f"start training with request:\n{request}")
        x_train = np.load(request.training_data_filename)['arr_0']
        y_labels = np.load(request.training_labels_filename)['arr_0']
        print(f"data loading completed x_train:{len(x_train)} y_labels:{len(y_labels)}")
        split_border = int(len(x_train) * request.validation_ratio)
        print(f"split border: {split_border}")
        x_val = x_train[:split_border]
        partial_x_train = x_train[split_border:]
        y_val = y_labels[:split_border]
        partial_y_train = y_labels[split_border:]

        print("start model.fit()")
        history = self.model.fit(x=partial_x_train, y=partial_y_train, epochs=request.epochs,
                                 batch_size=request.batch_size, validation_data=(x_val, y_val), callbacks=[tensorboard_callback])
        print(f"training finished with accuracy={history.history['accuracy'][-1]} and validation_loss={history.history['val_loss'][-1]}")
        self.model.save(request.model_filename)
        print(f"model saved to {request.model_filename}")


        response = news_classifier_pb2.TrainingStatus()
        response.accuracy = history.history['accuracy'][-1]
        response.validation_loss = history.history['val_loss'][-1]
        response.status_text = 'success'
        return response

    def classify(self, request, context):
        response = news_classifier_pb2.NewsCategory()
        maxlen = 10000
        words = request.text.split()
        news_indexed = []
        for word in words:
            if word not in word_index:
                news_indexed.append(2)
            else:
                news_indexed.append(word_index[word] + 3)

        news_padded = sequence.pad_sequences([news_indexed], truncating='pre', padding='pre', maxlen=maxlen)
        prediction = self.model.predict(news_padded)
        response.category_code=np.argmax(prediction)
        response.category_text=topic_map[response.category_code]
        return response

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
news_classifier_pb2_grpc.add_NewsClassifierServicer_to_server(NewsClassifier(), server)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
