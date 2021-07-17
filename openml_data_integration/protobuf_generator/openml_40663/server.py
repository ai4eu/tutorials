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

        response.Feature00                      = numpy.uint32(row[0])
        response.Feature01                      = numpy.uint32(row[1])
        response.Feature02                      = row[2]
        response.Feature03                      = row[3]
        response.Feature04                      = numpy.uint32(row[4])
        response.Feature05                      = row[5]
        response.Feature06                      = numpy.uint32(row[6])
        response.Feature07                      = numpy.uint32(row[7])
        response.Feature08                      = row[8]
        response.Feature09                      = row[9]
        response.Feature10                      = row[10]
        response.Feature11                      = row[11]
        response.Feature12                      = numpy.uint32(row[12])
        response.Feature13                      = numpy.uint32(row[13])
        response.Feature14                      = row[14]
        response.Feature15                      = row[15]
        response.Feature16                      = row[16]
        response.Feature17                      = row[17]
        response.Feature18                      = numpy.uint32(row[18])
        response.Feature19                      = numpy.uint32(row[19])
        response.Feature20                      = row[20]
        response.Feature21                      = numpy.uint32(row[21])
        response.Feature22                      = row[22]
        response.Feature23                      = numpy.uint32(row[23])
        response.Feature24                      = row[24]
        response.Feature25                      = row[25]
        response.Feature26                      = row[26]
        response.Feature27                      = row[27]
        response.Feature28                      = row[28]
        response.Feature29                      = row[29]
        response.Feature30                      = numpy.uint32(row[30])
        response.Feature31                      = row[31]
        response.Class                          = row[32]

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
