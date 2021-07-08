# date: 2021.03.30
# author: Han Tran htran@know-center.at

from concurrent import futures
import logging

import grpc

import model_pb2
import model_pb2_grpc

import classifier_model_pb2
import classifier_model_pb2_grpc
import pandas as pd

import utils
import myconstants

from sklearn.ensemble import RandomForestClassifier

port_address = myconstants.PORT_ADDRESS
port_address_classifier = myconstants.PORT_ADDRESS_CLASSIFIER
idx = myconstants.DATA_ID # fixed ID for data request

class ClassifierServicer(classifier_model_pb2_grpc.ClassifierServicer):

    def _get_data(self, request):
        try:
          self.df
        except:
          # self.df not yet initialized, do get the data
          # idx = request.idx # fixed when Empty msg sent
          with grpc.insecure_channel(f'localhost:{port_address}') as channel:
              stub = model_pb2_grpc.ExampleStub(channel)
              self.df, self.labels = utils.list_features(stub, idx=idx)

    def _get_prediction(self, value):
        clf = RandomForestClassifier()
        clf.fit(self.df, self.labels.values)
        label = clf.predict([value])
        return label

    def GetFeatureNames(self, request, context):
        print(f'\nGettingFeatureNames -- Request DataID: {request.idx}')
        self._get_data(request)
        return classifier_model_pb2.FeatureNames(feature_names=','.join(self.df.columns))



    def GetPrediction(self, request, context):
        idx = request.idx
        print(f'Request.idx is {idx}')
        value = request.request.split(',')
        print(f'GettingPrediction -- Request Values: {value}')

        self._get_data(request.idx)
        if len(value) != len(self.df.columns):
            return_text = f'''The number of values input {{{len(value)}}} does not match 
                            the given dataset {{{len(self.df.columns)}}}'''
            return classifier_model_pb2.ClassifierResult(label=return_text)

        label = self._get_prediction(value)
        print(f'Classifier result is: {str(label)}')
        return classifier_model_pb2.ClassifierResult(label=str(label))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    classifier_model_pb2_grpc.add_ClassifierServicer_to_server(
                                ClassifierServicer(), server)
    server.add_insecure_port(f'[::]:{port_address_classifier}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Starting classifier server")
    logging.basicConfig()
    serve()
