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
        # This is for OpenML dataset # 10
        ###############################################################

        response.Lymphatics                     = row[0]
        response.Block_of_affere                = row[1]
        response.Bl_of_lymph_c                  = row[2]
        response.Bl_of_lymph_s                  = row[3]
        response.By_pass                        = row[4]
        response.Extravasates                   = row[5]
        response.Regeneration_of                = row[6]
        response.Early_uptake_in                = row[7]
        response.Lym_nodes_dimin                = numpy.uint32(row[8])
        response.Lym_nodes_enlar                = numpy.uint32(row[9])
        response.Changes_in_lym                 = row[10]
        response.Defect_in_node                 = row[11]
        response.Changes_in_node                = row[12]
        response.Changes_in_stru                = row[13]
        response.Special_forms                  = row[14]
        response.Dislocation_of                 = row[15]
        response.Exclusion_of_no                = row[16]
        response.No_of_nodes_in                 = numpy.uint32(row[17])
        response.Class                          = row[18]

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
