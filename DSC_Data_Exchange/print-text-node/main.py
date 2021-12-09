from src import grpc_server
import logging

grpc_host = "[::]"
grpc_port = 8061

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    grpc_server.start_server(grpc_host, grpc_port)


if __name__ == '__main__':
    logging.basicConfig()
    main()
