# Telemetry Pipeline: Kafka on Kubernetes

A real-time pipeline that streams simulated server and cluster metrics through Kafka on Kubernetes, scales consumers automatically under load, and survives failures without losing data.

> Status: in progress. Results below are filled in as each phase is completed.

## Architecture

```
Producers (simulated hosts)
        |  keyed by host_id
        v
Kafka (Strimzi, 3 brokers)  -- topics: metrics, alerts
        |
        v
Consumers (rolling stats + anomaly detection, autoscaled by KEDA)
        |                         |
        v                         v
   Postgres (results)        alerts topic -> Alert service

Prometheus + Grafana watch the pipeline itself (throughput, lag, latency).
```

Everything runs on a local Kubernetes cluster (kind).

## Data

Each message is one reading from one simulated server:

```json
{
  "host_id": "web-042",
  "cluster": "us-east-1a",
  "timestamp": "2026-12-20T14:03:22.481Z",
  "cpu_pct": 71.4,
  "mem_pct": 63.8,
  "disk_io_mbps": 112.5,
  "net_rx_mbps": 48.2,
  "p99_latency_ms": 184.0,
  "error_rate_pct": 0.4
}
```

Injected anomalies: CPU pinned at 100%, memory leaks, cluster-wide latency and error spikes, and hosts going silent.

## Roadmap

- [ ] Phase 0: Kafka and Kubernetes tutorials
- [ ] Phase 1: Local pipeline with Docker Compose (producer, Kafka, consumer, Postgres)
- [ ] Phase 2: Run on Kubernetes with kind and Strimzi
- [ ] Phase 3: Anomaly detection and an alerts topic
- [ ] Phase 4: Autoscale consumers on Kafka lag with KEDA
- [ ] Phase 5: Failure testing (kill pods and brokers, verify zero data loss)
- [ ] Phase 6: Prometheus and Grafana dashboards
- [ ] Phase 7: Batch analytics with Spark over Parquet on MinIO
- [ ] Phase 8: Small MCP server so AI agents can query pipeline health
- [ ] Stretch: Rust consumer benchmarked against Python

## Results

| Metric | Value |
| --- | --- |
| Throughput (messages/sec) | TBD |
| End-to-end latency, p99 (ms) | TBD |
| Consumer scale-up time under load spike (s) | TBD |
| Recovery time after pod/broker failure (s) | TBD |
| Messages lost during failure tests | TBD |

## Stack

Python (confluent-kafka), Apache Kafka (Strimzi), Kubernetes (kind), Postgres, KEDA, Prometheus, Grafana, Apache Spark, MinIO

## Running locally

Setup instructions will be added as each phase is built.

## Design

See [docs/design.md](docs/design.md) for architecture decisions, tradeoffs, and failure scenarios.
