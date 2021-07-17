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

        response.Tr                             = row[0]
        response.Tree                           = row[1]
        response.Br                             = row[2]
        response.Tl                             = row[3]
        response.In                             = numpy.uint32(row[4])
        response.Internode_1                    = row[5]
        response.Internode_2                    = row[6]
        response.Internode_3                    = row[7]
        response.Internode_4                    = row[8]
        response.Internode_5                    = row[9]
        response.Internode_6                    = row[10]
        response.Internode_7                    = row[11]
        response.Internode_8                    = row[12]
        response.Internode_9                    = row[13]
        response.Internode_10                   = row[14]
        response.Internode_11                   = row[15]
        response.Internode_12                   = row[16]
        response.Internode_13                   = row[17]
        response.Internode_14                   = row[18]
        response.Internode_15                   = row[19]
        response.Internode_16                   = row[20]
        response.Internode_17                   = row[21]
        response.Internode_18                   = row[22]
        response.Internode_19                   = row[23]
        response.Internode_20                   = row[24]
        response.Internode_21                   = row[25]
        response.Internode_22                   = row[26]
        response.Internode_23                   = row[27]
        response.Internode_24                   = row[28]
        response.Internode_25                   = row[29]
        response.Internode_26                   = row[30]
        response.Internode_27                   = row[31]
        response.Internode_28                   = row[32]
        response.Internode_29                   = row[33]

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
