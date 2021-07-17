
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
