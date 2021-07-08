from __future__ import print_function
import logging
import sys
import grpc
import pandas as pd
import classifier_model_pb2
import classifier_model_pb2_grpc

import myconstants


id_default = myconstants.DATA_ID
port_address_classifier = myconstants.PORT_ADDRESS_CLASSIFIER

def get_feature_names(stub, idx=id_default):
    response = stub.GetFeatureNames(classifier_model_pb2.DataID(idx=idx)).feature_names
    return response


def get_prediction(stub, features):
    idx = features[0]
    request = ','.join([str(i) for i in features[1]])
    response = stub.GetPrediction(classifier_model_pb2.Request(idx=
                                    classifier_model_pb2.DataID(idx=idx),
                                    request=request)).label
    return response


def main(argv):
    with grpc.insecure_channel(f'localhost:{port_address_classifier}') as channel:
        stub = classifier_model_pb2_grpc.ClassifierStub(channel)
        try:
            idx = int(argv[0]) # input direct
        except:
            idx = id_default

        # get feature names
        feature_names = get_feature_names(stub, idx=idx).split(',')
        print(f'Dataset with ID {idx} has {len(feature_names)} features with names as below:\
                \n\t {feature_names}\n')

        # Values for set 61
        values = [5.1, 3.5, 1.4, 0.5]    # Prediction is Iris-setosa
        #values = [1.0, 2.0, 3.0, 1.0]    # Prediction is Iris-versicolor

        # Values for set 6
        #values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]   # Prediction is typically 'C'
        #values = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]          # Prediction should be 'A'
        #values = [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]   # Prediction is typically 'N'

        # get prediction
        result = get_prediction(stub, [idx, values])
        print(f'The prediction for {values} is:\n {result}\n\n')


if __name__ == '__main__':
    logging.basicConfig()
    main(sys.argv[1:])
