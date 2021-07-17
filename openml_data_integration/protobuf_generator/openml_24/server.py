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

        response.Cap_shape                      = row[0]
        response.Cap_surface                    = row[1]
        response.Cap_color                      = row[2]
        response.Bruises_3f                     = row[3]
        response.Odor                           = row[4]
        response.Gill_attachment                = row[5]
        response.Gill_spacing                   = row[6]
        response.Gill_size                      = row[7]
        response.Gill_color                     = row[8]
        response.Stalk_shape                    = row[9]
        response.Stalk_root                     = row[10]
        response.Stalk_surface_above_ring       = row[11]
        response.Stalk_surface_below_ring       = row[12]
        response.Stalk_color_above_ring         = row[13]
        response.Stalk_color_below_ring         = row[14]
        response.Veil_type                      = row[15]
        response.Veil_color                     = row[16]
        response.Ring_number                    = row[17]
        response.Ring_type                      = row[18]
        response.Spore_print_color              = row[19]
        response.Population                     = row[20]
        response.Habitat                        = row[21]
        response.Class                          = row[22]

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
