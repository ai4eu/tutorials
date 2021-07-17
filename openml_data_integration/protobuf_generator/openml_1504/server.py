# date: 2021.07.14
# author: Raul Saavedra raul.saavedra.felipe@iais.fraunhofer.de

import grpc
from concurrent import futures
import time
import numpy

# import constant with the hardcoded openml data ID number
import myconstants

# import the generated grpc related classes for python
import model_pb2
import model_pb2_grpc

# import utility file to get the data
import openml_data_fetcher as odf

port_address = 8061
openml_obj = odf.FetchOpenMLData()
current_row = 0

class get_next_rowServicer(model_pb2_grpc.get_next_rowServicer):
    def get_next_row(self, request, context):
        response = model_pb2.Features()
        total_rows = openml_obj.get_num_rows()
        current_row = openml_obj.current_row
        #print("total number of rows of OpenML file: ", total_rows)
        if current_row == total_rows:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('All available data has been processed')
            print("All data processed. Exception raised")
            return response

        #print(f"fetching row {current_row} from a total of {total_rows}")
        row = openml_obj.get_next_row(current_row)
        openml_obj.current_row = openml_obj.current_row + 1

        ###############################################################
        # Here goes the OpenML dataset specific Feature assignments
        ###############################################################

        response.V1                             = row[0]
        response.V2                             = row[1]
        response.V3                             = row[2]
        response.V4                             = row[3]
        response.V5                             = row[4]
        response.V6                             = row[5]
        response.V7                             = row[6]
        response.V8                             = row[7]
        response.V9                             = numpy.uint32(row[8])
        response.V10                            = numpy.uint32(row[9])
        response.V11                            = row[10]
        response.V12                            = numpy.uint32(row[11])
        response.V13                            = numpy.uint32(row[12])
        response.V14                            = row[13]
        response.V15                            = row[14]
        response.V16                            = row[15]
        response.V17                            = row[16]
        response.V18                            = row[17]
        response.V19                            = row[18]
        response.V20                            = row[19]
        response.V21                            = row[20]
        response.V22                            = row[21]
        response.V23                            = row[22]
        response.V24                            = row[23]
        response.V25                            = row[24]
        response.V26                            = row[25]
        response.V27                            = row[26]
        response.V28                            = numpy.uint32(row[27])
        response.V29                            = numpy.uint32(row[28])
        response.V30                            = numpy.uint32(row[29])
        response.V31                            = numpy.uint32(row[30])
        response.V32                            = numpy.uint32(row[31])
        response.V33                            = numpy.uint32(row[32])
        response.Class                          = row[33]

        ###############################################################
        return response


# Following House_Price_Prediction/csv_databroker/csv_server.py
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
model_pb2_grpc.add_get_next_rowServicer_to_server(get_next_rowServicer(), server)
print("Starting OpenML data node server")
server.add_insecure_port(f'[::]:{port_address}')
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
