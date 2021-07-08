# date: 2021.03.30
# author: Han Tran htran@know-center.at

from concurrent import futures
import logging

import grpc
import model_pb2
import model_pb2_grpc
import openml as oml
import pandas as pd
import myconstants

port_address = myconstants.PORT_ADDRESS

def get_data(idx):
    try:
        dataset = oml.datasets.get_dataset(idx);
        return dataset
    except:
        print(f'Not found {idx}')
        return

class ExampleServicer(model_pb2_grpc.ExampleServicer):

    def PullData(self, request, context):
        # idx = request.idx
        idx = myconstants.DATA_ID
        print(f'Getting data with ID: {idx}')
        dataset = get_data(int(idx))
        if not dataset: return
        data = dataset.get_data()
        ncols = len(data[0].dtypes)
        descr = dataset.description[:400].split("\n")
        print(f'\n\nDataset ID    : {idx}')
        print(f'Dataset Name  : {dataset.name}')
        print(f'Dataset URL   : {dataset.url}')
        print(f'Num. Columns  : {ncols}')
        print(f'********** Beginning of Dataset description **********')
        for line in descr:
            if line.strip() != "":
                print(f'{line[:80]}')
        print(f'******************************************************')

        df = data[0]
        label2 = 'class'
        try:
            df_label = df.loc[:, [label2]].shape[1]
        except:
            df_label = 0
        if df_label == 1:
            label1 = str(df[label2].dtypes)
            labels = df[label2]
            df = df.drop(label2, axis=1)
            record1 = ','.join([str(i) for i in df.dtypes])
        else:
            record1 = ','.join([str(i) for i in df.dtypes])
            label2 = label1 = ''
            labels = pd.Series('', index=df.index)

        # types of features
        yield model_pb2.Response(record=record1, label=label1)
        #print(f'record1 = {record1}')
        #print(f'label1  = {label1}')

        # feature names incl. class
        yield model_pb2.Response(record=','.join(df.columns), label=label2)
        print(f'Feature names:')
        print(f','.join(df.columns))

        # data, labels
        #print(f'Data, labels:')
        for idx, row in enumerate(df.values.tolist()):
            yield model_pb2.Response(record=','.join([str(i) for i in row]),
                label=labels[idx])
            #print(f', '.join([str(i) for i in row]) + ' -- ' + labels[idx])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_ExampleServicer_to_server(
        ExampleServicer(), server)
    server.add_insecure_port(f'[::]:{port_address}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Starting data node server")
    logging.basicConfig()
    serve()
