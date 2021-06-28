import grpc
from concurrent import futures
import time
import news_databroker_pb2_grpc
import news_databroker_pb2

port = 8061

news = [
    'In Hong Kong, where newspapers have alleged Japan has been selling below-cost semiconductors, some electronics manufacturers share that view.',
    'The Ministry of International Trade and Industry (MITI) will revise its long-term energy supply/demand outlook by August to meet a forecast downtrend in Japanese energy demand, ministry officials said.',
    'Thailands trade deficit widened to 4.5 billion baht in the first quarter of 1987 from 2.1 billion a year ago, the Business Economics Department said.',
    'Prices of Malaysian and Sumatran CPO are now around 332 dlrs a tonne CIF for delivery in Rotterdam, traders said.',
    'Victoria and Western Australia yesterday lifted their ban on foreign-flag ships carrying containers but NSW ports are still being disrupted by a separate dispute, shipping sources said.',
    'He told Reuters in a telephone interview that trading in palm oil, sawn timber, pepper or tobacco was being considered.',
    'SRI LANKA GETS USDA APPROVAL FOR WHEAT PRICE',
    'Osaka-based Sumitomo, with desposits of around 23.9 trillion yen, merged with Heiwa Sogo, a small, struggling bank with an estimated 1.29 billion dlrs in unrecoverable loans, in October.',
    'Asked by Reuters to clarify his statement on Monday in which he said the pact should be allowed to lapse, Subroto said Indonesia was ready to back extension of the ITA.',
    'Banks, which bid for a total 12.2 billion marks liquidity, will be credited with the funds allocated today and must buy back securities pledged on May 6.']


class NewsDatabroker(news_databroker_pb2_grpc.NewsDatabrokerServicer):

    def __init__(self):
        self. current_row = 0

    def get_next(self, request, context):
        response = news_databroker_pb2.NewsText()
        if self.current_row >= len(news):
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("all data has been processed")
        else:
            response.text = news[self.current_row]
            self.current_row += 1

        return response


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
news_databroker_pb2_grpc.add_NewsDatabrokerServicer_to_server(NewsDatabroker(), server)
print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
