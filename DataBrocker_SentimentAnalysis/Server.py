import grpc
from concurrent import futures
import time

# import the generated classes :
import model_pb2
import model_pb2_grpc

import get_next_row as gnr

port = 50059
row_obj = gnr.FetchRowCSV()
current_row = 0


class get_next_rowServicer(model_pb2_grpc.get_next_rowServicer):
    # row_obj = gnr.FetchRowCSV()
    def get_next_row(self, request, context):
        response = model_pb2.Features()
        total_rows = row_obj.init_count()
        current_row = row_obj.current_row
        print("total number of rows of csv: ", total_rows)
        if current_row % total_rows == 0 and current_row != 0:
            response.row_Number = float(0)
            response.text = str("")
            response.polarity = float(0)
        else:
            print("entered else:")
            row = row_obj.get_next_row(current_row)
            response.row_Number = row[0]
            response.text = row[1]
            response.polarity = row[2]
            row_obj.current_row = row_obj.current_row + 1

        return response


if __name__ == '__main__':

    # creat a grpc server :
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    model_pb2_grpc.add_get_next_rowServicer_to_server(get_next_rowServicer(), server)
    print("Starting Server. Listening to port :" + str(port))
    server.add_insecure_port("[::]:{}".format(port))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
