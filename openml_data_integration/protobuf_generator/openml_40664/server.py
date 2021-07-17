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

        response.Class                          = row[0]
        response.Buying_price_vhigh             = row[1]
        response.Buying_price_high              = row[2]
        response.Buying_price_med               = row[3]
        response.Buying_price_low               = row[4]
        response.Maintenance_price_vhigh        = row[5]
        response.Maintenance_price_high         = row[6]
        response.Maintenance_price_med          = row[7]
        response.Maintenance_price_low          = row[8]
        response.Doors_2                        = row[9]
        response.Doors_3                        = row[10]
        response.Doors_4                        = row[11]
        response.Doors_5more                    = row[12]
        response.Persons_2                      = row[13]
        response.Persons_4                      = row[14]
        response.Persons_more                   = row[15]
        response.Luggage_boot_size_small        = row[16]
        response.Luggage_boot_size_med          = row[17]
        response.Luggage_boot_size_big          = row[18]
        response.Safety_low                     = row[19]
        response.Safety_med                     = row[20]
        response.Safety_high                    = row[21]

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
