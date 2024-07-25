import os
import uuid
import json
import numpy as np
import grpc
import bloom_service_pb2_grpc
from bloom_service_pb2 import InputMessage, OutputMessage
from dotenv import load_dotenv

load_dotenv()

SERVER_HOST = os.environ.get("HOST", "localhost")
SERVER_PORT = int(os.environ.get("PORT", 5000))
CHANNEL_IP = f"{SERVER_HOST}:{SERVER_PORT}"

if __name__ == "__main__":
    channel = grpc.insecure_channel(CHANNEL_IP)
    stub = bloom_service_pb2_grpc.BloomServiceStub(channel)

    while True:
        text = input("What do ya wanna ask? ('!q' to quit) >> ")

        if text == "!q":
            break

        request = InputMessage(prompt=text)

        responses = stub.Chat(request)
        for response in responses:
            print(f"Response: {response.partial}, (p={response.prob})")