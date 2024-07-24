GRPC_SOURCES_BLOOM_SERVICE = bloom_service_pb2.py bloom_service_pb2_grpc.py

all: $(GRPC_SOURCES_BLOOM_SERVICE)

$(GRPC_SOURCES_BLOOM_SERVICE): bloom_service.proto
	python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. bloom_service.proto

clean:
	rm $(GRPC_SOURCES_BLOOM_SERVICE)
	