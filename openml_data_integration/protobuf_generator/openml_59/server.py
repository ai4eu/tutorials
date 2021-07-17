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

        response.A01                            = numpy.uint32(row[0])
        response.A02                            = numpy.uint32(row[1])
        response.A03                            = row[2]
        response.A04                            = row[3]
        response.A05                            = row[4]
        response.A06                            = row[5]
        response.A07                            = row[6]
        response.A08                            = row[7]
        response.A09                            = row[8]
        response.A10                            = row[9]
        response.A11                            = row[10]
        response.A12                            = row[11]
        response.A13                            = row[12]
        response.A14                            = row[13]
        response.A15                            = row[14]
        response.A16                            = row[15]
        response.A17                            = row[16]
        response.A18                            = row[17]
        response.A19                            = row[18]
        response.A20                            = row[19]
        response.A21                            = row[20]
        response.A22                            = row[21]
        response.A23                            = row[22]
        response.A24                            = row[23]
        response.A25                            = row[24]
        response.A26                            = row[25]
        response.A27                            = row[26]
        response.A28                            = row[27]
        response.A29                            = row[28]
        response.A30                            = row[29]
        response.A31                            = row[30]
        response.A32                            = row[31]
        response.A33                            = row[32]
        response.A34                            = row[33]
        response.Class                          = row[34]

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
