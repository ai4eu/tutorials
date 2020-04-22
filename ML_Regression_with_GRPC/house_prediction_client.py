import grpc
from random import randint
from timeit import default_timer as timer

# import the generated classes
import model_pb2
import model_pb2_grpc

start_ch = timer()

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')
# create a stub (client)
stub = model_pb2_grpc.PredictStub(channel)
end_ch = timer()
MSSubClass   = [randint(1,11) for i in range(0,1000)]
LotArea      = [randint(100,1500) for i in range(0,1000)]
YearBuilt    = [randint(1915,2000) for i in range(0,1000)]
BedroomAbvGr = [randint(2,10) for i in range(0,1000)]
TotRmsAbvGrd = [randint(2,12) for i in range(0,1000)]
ans_lst = []
start = timer()
for i in range(0,len(MSSubClass)-1):
    # create a valid request message
    requestPrediction  = model_pb2.Features(MSSubClass = MSSubClass[i], LotArea = LotArea[i],
                                        YearBuilt = YearBuilt[i], BedroomAbvGr = BedroomAbvGr[i],
                                        TotRmsAbvGrd = TotRmsAbvGrd[i])
    # make the call
    responsePrediction = stub.predict_sale_price(requestPrediction)
    ans_lst.append(responsePrediction.salePrice)
    print('The prediction is :',responsePrediction.salePrice)
print('Done!')
end = timer()
all_time = end - start
ch_time = end_ch - start_ch
print ('Time spent for {} predictions is {}'.format(len(MSSubClass),(all_time)))
print('In average, {} second for each prediction'.format(all_time/len(MSSubClass)))
print('That means you can do {} predictions in one second'.format(int(1/(all_time/len(MSSubClass)))))
print('Time for connecting to server = {}'.format(ch_time))
