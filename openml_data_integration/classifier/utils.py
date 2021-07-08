# date: 2021.03.30
# author: Han Tran htran@know-center.at

import grpc

import model_pb2
import model_pb2_grpc
import pandas as pd
import myconstants

def list_features(stub, idx):
    idx = myconstants.DATA_ID
    # features = stub.PullData(model_pb2.DataID(idx=idx))
    features = stub.PullData(model_pb2.Empty())
    df = pd.DataFrame()
    labels = pd.Series(dtype='object')
    try:
        data = []
        label = []
        for i, row in enumerate(features):
            data.append(row.record.split(','))
            label.append(row.label)
        columns = data[1]
        types = data[0]
        df = pd.DataFrame(data[2:], columns=columns)
        if label[1] != '':
            labels = pd.Series(label[2:], name=label[1], dtype=label[0])
        for i, c in enumerate(df.columns):
            df[c] = df[c].astype(types[i])
    except:
        print(f'Sorry, No data with ID {idx} found.')

    return df, labels
