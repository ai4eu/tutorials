import threading

from src import grpc_server
from src.flask_server import run_flask_app
import logging

from src.state.configuration_state import Configuration

grpc_port = 8061
flask_host = "0.0.0.0"
flask_port = 8062

conf = Configuration()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def main():
    server = grpc_server.start_server(grpc_port, conf)
    flask_server_thread = threading.Thread(target=run_flask_app, args=(flask_host, flask_port, conf,))
    flask_server_thread.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    main()
