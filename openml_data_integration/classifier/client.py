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

        # get prediction
        values = [6.2, 1.4, 5.4, 2.3]
        result = get_prediction(stub, [idx, values])
        print(f'The prediction for {values} is:\n {result}\n\n')


if __name__ == '__main__':
    logging.basicConfig()
    main(sys.argv[1:])