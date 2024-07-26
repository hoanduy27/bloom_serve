# bloom serve

Serving BloomZ. Supports:

- Streaming LLM

- KV Caching

- Token probability logging

- Benchmarking throughput and latency at different CCUs.

Model uses: [BloomZ-1b1 (quantized)](https://huggingface.co/hoanduy27)
Prebuild: [Docker image](https://hub.docker.com/repository/docker/hoanduy27/bloomz-service/general)

# Quick start (hope so)

- Start the server
```sh
    docker compose up -d
```

- Setup client environment

```
    cp .env.development .env
    pip install -r requirements-client.txt
```

Or simply

```
    ./setup_client.sh
```

- Run the client

```sh
    python test.py
```

- (Optional) benchmarking throughput and latency

```sh
    python -m monitor.benchmark <number_of_concurrent_requests>
```
