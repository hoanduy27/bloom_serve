import os
import json
import logging
import grpc
import io
import grpc.experimental
import bloom_service_pb2
import bloom_service_pb2_grpc
from bloom_service_pb2 import (
    InputMessage,
    OutputMessage,
)
from concurrent import futures

from dotenv import load_dotenv

from model import BloomInferencer

load_dotenv()


class BloomService(bloom_service_pb2_grpc.BloomService):
    def __init__(self, model_path):
        self.inferencer = BloomInferencer.from_pretrained(model_path)

    def Chat(self, request, context):
        logging.info(f"Received: {request.prompt}")

        text = request.prompt
        for partial, prob in self.inferencer(text):
            yield OutputMessage(
                partial=partial,
                prob=prob,
            )


def serve():
    model_path = os.environ.get("CHECKPOINT", None)
    service_port = os.environ.get("PORT", 50001)
    grpc_max_workers = int(os.environ.get("GRPC_MAX_WORKERS", 6))
    grpc_max_concurrent_rpcs = int(os.environ.get("GRPC_MAX_CONCURRENT_RPC", 6))

    options = [
        ("grpc.max_receive_message_length", 1166528012),
        ("grpc.max_send_message_length", 1166528012),
    ]

    server = grpc.server(
        # futures.ThreadPoolExecutor(),
        futures.ThreadPoolExecutor(max_workers=grpc_max_workers),
        maximum_concurrent_rpcs=grpc_max_concurrent_rpcs,
        options=options,
    )

    bloom_service_pb2_grpc.add_BloomServiceServicer_to_server(
        BloomService(model_path), server
    )
    server.add_insecure_port(f"[::]:{service_port}")
    server.start()
    logging.info("Start bloom service")
    logging.info(f"Started gRPC server on localhost:{service_port}")
    server.wait_for_termination()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
