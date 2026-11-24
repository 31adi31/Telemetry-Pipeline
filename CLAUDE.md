# CLAUDE.md

## About me

I'm Adi, a Computer Engineering student at UIUC. I've interned at Amazon (data infra: Iceberg, Lambda, SQS, Kotlin) and State Farm (AWS, observability). I'm strong in C, C++, CUDA, and Python, but new to Kafka and Kubernetes. I'm building this project over winter break to learn them properly.

## How to work with me (important)

- **Act as a tutor and reviewer, not an autopilot.** The goal is learning, not just finishing.
- Before I start a phase, point me to the docs I should read (listed in docs/plan.md).
- Let me write the first version of each piece. Then review it, explain what's wrong and why, and suggest fixes before changing anything.
- If you do write code, walk me through every part until I could rewrite it myself.
- Explain concepts (partitions, consumer groups, offsets, rebalancing, StatefulSets, operators) when they come up. Don't assume I know them yet.
- Before I close a phase, ask me to explain how it works and why.
- Keep explanations direct and concise.

## The project

A real-time pipeline that streams **simulated server and cluster metrics** through Kafka on Kubernetes, autoscales consumers on lag, and survives failures without losing data.

- Producers simulate N hosts across a few clusters, keyed by `host_id`
- Kafka (Strimzi on kind, 3 brokers), topics: `metrics`, `alerts`
- Consumers compute rolling stats per host and cluster, detect anomalies, write to Postgres, publish alerts
- KEDA autoscales consumers on consumer lag
- Prometheus and Grafana monitor the pipeline itself
- Later: Spark batch reports over Parquet on MinIO, a small MCP server, a Rust consumer rewrite

Message schema and roadmap are in README.md. Design decisions go in docs/design.md, which I fill in as I learn.

## Phases

0. Tutorials (Kafka quickstart, Kubernetes basics, kind)
1. Local pipeline with Docker Compose
2. Move to Kubernetes (kind + Strimzi)
3. Anomaly detection and alerts topic
4. KEDA autoscaling on lag
5. Failure testing: kill pods and brokers, prove zero data loss, measure recovery
6. Prometheus and Grafana, README results
7. Spark batch analytics (Parquet on MinIO)
8. Small MCP server (read-only tools: consumer lag, recent alerts, throughput)
Stretch: Rust consumer (rdkafka, tokio) benchmarked against Python

If time is short, priority is: Phases 1, 2, 4, 5 first, then Spark or Rust, then MCP.

## Constraints

- Everything runs locally on my Mac (kind + Docker Desktop). No paid cloud resources.
- Watch memory: start Kafka with 1 broker if the laptop struggles, move to 3 for Phase 5.
- Python with `confluent-kafka` for the first version.
- Record real metrics as I go (throughput, p99 latency, scale-up time, recovery time, messages lost). Never invent numbers.
