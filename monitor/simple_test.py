import os
import time
import concurrent.futures
import grpc
import bloom_service_pb2_grpc
from bloom_service_pb2 import InputMessage
from dotenv import load_dotenv
from monitor.text import questions
import sys
import random 

load_dotenv()

SERVER_HOST = os.environ.get("HOST", "localhost")
SERVER_PORT = int(os.environ.get("PORT", 5000))
CHANNEL_IP = f"{SERVER_HOST}:{SERVER_PORT}"

def send_request(stub, text):
    request = InputMessage(prompt=text)
    responses = stub.Chat(request)
    first_chunk_time = None
    word_count = 0
    
    start_time = time.time()
    for response in responses:
        if first_chunk_time is None:
            first_chunk_time = time.time()
            latency = first_chunk_time - start_time
        word_count += 1
        print(f"Response: {response.partial}, (p={response.prob})")
    end_time = time.time()

    throughput = word_count / (end_time - start_time)
    
    return latency, throughput

if __name__ == "__main__":
    n = int(sys.argv[1])

    channel = grpc.insecure_channel(CHANNEL_IP)
    stub = bloom_service_pb2_grpc.BloomServiceStub(channel)
    
    
    latencies = []
    throughputs = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
        futures = [] 

        for i in range(n):
            text = random.choice(questions) 
            futures.append(executor.submit(send_request, stub, text))

        for future in concurrent.futures.as_completed(futures):
            latency, throughput = future.result()
            latencies.append(latency)
            throughputs.append(throughput)
    
    avg_latency = sum(latencies) / n
    avg_throughput = sum(throughputs) / n
    
    print(f"Average Latency: {avg_latency:.4f} seconds")
    print(f"Average Throughput: {avg_throughput:.2f} words/second")
