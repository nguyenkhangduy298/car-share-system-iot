# Reference: https://grpc.io/docs/quickstart/python.html#update-a-grpc-service
# Repository: https://github.com/grpc/grpc
from __future__ import print_function
import logging
import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)

        response = stub.SayHello(helloworld_pb2.HelloRequest(name = "Matthew"))
        print("Greeter client received: " + response.message)

        response = stub.SayHelloAgain(helloworld_pb2.HelloRequest(name = "Matthew"))
        print("Greeter client received: " + response.message)

if __name__ == "__main__":
    logging.basicConfig()
    run()
