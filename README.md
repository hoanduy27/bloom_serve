# bloom serve

<div>
    <a href="https://huggingface.co/hoanduy27/bloomz-1b1-quantization-nf4"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20HuggingFace-grey"></a>
    <a href="https://hub.docker.com/repository/docker/hoanduy27/bloomz-service/general"><img src="https://img.shields.io/badge/Docker-blue"></a>
</div>

Serving BloomZ. Supports:

- Streaming LLM

- KV Caching

- Token probability logging

- Benchmarking throughput and latency at different CCUs.

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
