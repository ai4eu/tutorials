import grpc
from concurrent import futures
import time
import news_trainer_pb2_grpc
import news_trainer_pb2
import os
import numpy as np
from tensorflow.keras.datasets import reuters
from tensorflow.keras.utils import to_categorical


def vectorize_sequences(sequences, dimension=10000):
    results = np.zeros((len(sequences), dimension))
    for i, sequence in enumerate(sequences):
        results[i, sequence] = 1.
    return results


port = 8061
shared_folder = os.getenv("SHARED_FOLDER_PATH")
print(f'shared_folder: {shared_folder}')
train_data_path = shared_folder+"/reuters_training_data.npz"
train_labels_path = shared_folder+"/reuters_training_labels.npz"
model_path = shared_folder+"/reuters_model.h5"

(train_data, train_labels), (test_data, test_labels) = reuters.load_data(num_words=10000)
word_index = reuters.get_word_index()
x_train = vectorize_sequences(train_data)
one_hot_train_labels = to_categorical(train_labels)
np.savez_compressed(train_data_path, x_train);
np.savez_compressed(train_labels_path, one_hot_train_labels);


class NewsTrainer(news_trainer_pb2_grpc.NewsTrainerServicer):

    def __init__(self):
        self.start_count = 0

    def startTraining(self, request, context):
        response = news_trainer_pb2.TrainingConfig()
        if self.start_count > 0:
            if self.start_count == 1:
                print("training already done.")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("training done.")
        else:
            print("start the training...")
            response.training_data_filename = train_data_path
            response.training_labels_filename = train_labels_path
            response.epochs = 9
            response.batch_size = 512
            response.validation_ratio = 0.1
            response.model_filename = model_path
        self.start_count += 1
        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
news_trainer_pb2_grpc.add_NewsTrainerServicer_to_server(NewsTrainer(), server)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
