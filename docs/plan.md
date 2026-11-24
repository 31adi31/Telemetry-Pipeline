# Kafka + Kubernetes Telemetry Pipeline: Project Plan

## Goal

Build a real-time pipeline that streams simulated server and cluster metrics through Kafka on Kubernetes, scales with load, and survives failures without losing data.

When it's done, the project should show four things an interviewer can check:

- **Streaming:** producers, topics, partitions, and consumer groups working end to end
- **Orchestration:** every service deployed and configured on Kubernetes
- **Scaling:** consumers that scale up automatically when they fall behind
- **Fault tolerance:** pods killed on purpose, with measured recovery and no lost messages

## How to use this with Claude Code

The goal is to learn, not just finish, so Claude Code is a tutor and reviewer, not an autopilot.

1. Read the phase's "Read first" docs before touching code.
2. Write the first version of each piece yourself, even if it's rough.
3. Ask Claude Code to review it, explain what's wrong, and why, before it changes anything.
4. When it writes code for you, ask it to walk through every part until you could rewrite it from memory.
5. Before closing a phase, explain the done criterion out loud: what happens, and why it works. If you can't, you're not done.

## Architecture

```
Producers (simulated hosts) --keyed by host_id--> Kafka (Strimzi, 3 brokers)
                                                    topics: metrics, alerts
                                                        |
                                    reads metrics       |      publishes alerts
                                                        v
                                    Consumers (rolling stats, anomaly checks, KEDA-scaled)
                                          |                          |
                                          v                          v
                                  Postgres (results)        Alert service (via alerts topic)

Prometheus + Grafana scrape the pipeline itself: throughput, lag, latency.
Everything runs in one local Kubernetes cluster (kind).
```

## Phase 0: Tutorials first

Do these before writing any project code. Aim for about a week total, at your own pace.

**Kafka**

- [ ] [Kafka Quickstart](https://kafka.apache.org/quickstart): run a broker locally, create a topic, produce and consume messages
- [ ] [Kafka docs: Design section](https://kafka.apache.org/documentation/#design): partitions, replication, the log, why Kafka is fast
- [ ] [Confluent Developer](https://developer.confluent.io): the Kafka 101 course for producers, consumers, consumer groups, and offsets
- [ ] Write a tiny Python producer and consumer with `confluent-kafka` against your local broker

**Kubernetes**

- [ ] [Kubernetes Basics tutorial](https://kubernetes.io/docs/tutorials/kubernetes-basics/): deploy, expose, scale, and update an app
- [ ] [Kubernetes Concepts](https://kubernetes.io/docs/concepts/): read Pods, Deployments, Services, ConfigMaps, StatefulSets
- [ ] Install [kind](https://kind.sigs.k8s.io) and `kubectl` on your Mac, and deploy a hello-world container

**You're ready for Phase 1 when** you can explain what a partition and a consumer group are, and you can deploy and scale a Deployment with `kubectl`.

## Build phases

Each phase ends with something working, so you can stop at any phase and still have a project.

### Phase 1: Pipeline on your laptop (Docker Compose)

Read first: [Kafka introduction](https://kafka.apache.org/intro) · [confluent-kafka Python client](https://docs.confluent.io/kafka-clients/python/current/overview.html) · [Docker Compose](https://docs.docker.com/compose/) · [psycopg 3](https://www.psycopg.org/psycopg3/docs/)

- [ ] Run Kafka and Postgres with Docker Compose
- [ ] Producer: simulates N servers across a few clusters sending metrics (host ID, cluster, timestamp, CPU, memory, disk and network I/O, p99 latency, error rate) at a set rate
- [ ] Pick a message key (host ID) so each host's readings stay ordered in one partition
- [ ] Consumer: reads the topic, computes rolling averages per host and cluster, writes results to Postgres
- [ ] Done when: data flows producer to Postgres and you can query results

### Phase 2: Move it onto Kubernetes

Read first: [kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/) · [Strimzi quickstarts](https://strimzi.io/quickstarts/) · [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) · [StatefulSets](https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/) · [ConfigMaps](https://kubernetes.io/docs/concepts/configuration/configmap/) · [Secrets](https://kubernetes.io/docs/concepts/configuration/secret/)

- [ ] Create a local cluster with kind
- [ ] Install the [Strimzi](https://strimzi.io) operator and deploy a Kafka cluster with it (1 broker if memory is tight, 3 by Phase 5)
- [ ] Containerize producer and consumer; deploy each as a Deployment
- [ ] Postgres as a StatefulSet with a persistent volume; config in ConfigMaps and Secrets
- [ ] Done when: the whole pipeline runs with `kubectl apply` and nothing on your laptop outside the cluster

### Phase 3: Anomaly detection and a second stream

Read first: [Kafka design: the consumer and offsets](https://kafka.apache.org/documentation/#design) · [Confluent Kafka 101 course](https://developer.confluent.io/courses/apache-kafka/events/)

- [ ] Consumer flags anomalies (CPU pinned at 100%, memory leaks, latency and error spikes, silent hosts) and publishes them to an `alerts` topic
- [ ] A small alert service consumes `alerts` and logs or stores them
- [ ] Done when: injected bad readings show up as alerts end to end

### Phase 4: Autoscaling

Read first: [KEDA Kafka scaler](https://keda.sh/docs/latest/scalers/apache-kafka/) · [Kubernetes Horizontal Pod Autoscaling](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/)

- [ ] Install [KEDA](https://keda.sh) and scale consumers on Kafka consumer lag
- [ ] Spike the producer rate and watch consumers scale up, then back down
- [ ] Done when: lag stays bounded under a load spike, and you have a graph of it

### Phase 5: Break it on purpose

Read first: [Kafka replication](https://kafka.apache.org/documentation/#replication) · [Producer acks setting](https://kafka.apache.org/documentation/#producerconfigs_acks) · [Kubernetes disruptions](https://kubernetes.io/docs/concepts/workloads/pods/disruptions/)

- [ ] Kill consumer pods mid-stream; confirm the group rebalances and no messages are lost
- [ ] Kill a Kafka broker; confirm replication keeps the topic available
- [ ] Use producer acks and consumer offset commits so you can prove no data loss, by counting messages sent versus stored
- [ ] Done when: you have recovery times and a message count that matches after each failure

### Phase 6: Observability and write-up

Read first: [Prometheus first steps](https://prometheus.io/docs/introduction/first_steps/) · [Grafana docs](https://grafana.com/docs/grafana/latest/) · [Strimzi docs (metrics section)](https://strimzi.io/documentation/)

- [ ] Expose metrics (throughput, lag, latency) with Prometheus and graph them in Grafana
- [ ] Update the README with the architecture diagram, how to run it, and your measured results

### Phase 7: Batch analytics with Spark

Read first: [MinIO docs](https://min.io/docs/) · [Spark: reading Parquet](https://spark.apache.org/docs/latest/sql-data-sources-parquet.html) · [Running Spark on Kubernetes](https://spark.apache.org/docs/latest/running-on-kubernetes.html) · [Spark Operator](https://github.com/kubeflow/spark-operator)

- [ ] Deploy MinIO in the cluster as S3-compatible storage
- [ ] Add a sink consumer that writes raw metrics to Parquet files in MinIO, partitioned by date
- [ ] Install the Spark Operator and run a Spark job that computes daily per-host and per-cluster health reports (average CPU and memory, p99 latency trends, anomaly counts)
- [ ] Schedule the job to run periodically instead of keeping Spark always on, to save laptop memory
- [ ] Done when: a scheduled Spark job reads a day of Parquet data and writes a report table to Postgres

### Phase 8 (small): MCP server for the pipeline

Read first: [Model Context Protocol docs](https://modelcontextprotocol.io) · [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) · [Connecting MCP servers to Claude Code](https://docs.claude.com/en/docs/claude-code/mcp)

- [ ] Build a small MCP server in Python with read-only tools: get consumer lag, query recent alerts from Postgres, get throughput from Prometheus
- [ ] Connect it to Claude Code and ask it to investigate a lag spike or an alert using real pipeline data
- [ ] Keep it to a few tools; this is a short final step, not a core phase
- [ ] Done when: an agent can answer "why did lag spike?" from live pipeline data

**If time runs short, do it in this order:** the core (Phases 1, 2, 4, 5), then Spark or the Rust consumer, then the MCP server.

## What to measure

Measured numbers are what turn this into a strong resume line, so record each one as you go.

| Metric | How to measure | Phase |
| --- | --- | --- |
| Throughput (messages/sec) | Messages stored per second at steady state | 1, 4 |
| End-to-end latency (ms) | Timestamp at produce vs. at write to Postgres, p50 and p99 | 1, 6 |
| Consumer lag | Kafka lag per partition under a load spike | 4 |
| Scale-up time (s) | Time from spike start to lag back under target | 4 |
| Recovery time (s) | Time from pod or broker kill to normal throughput | 5 |
| Data loss | Messages sent vs. stored after each failure (target: 0) | 5 |

Target resume bullets, with real numbers filled in:

- Built a real-time metrics pipeline on Kubernetes with Kafka (Strimzi) processing **X** messages/sec at **Y** ms p99 latency
- Autoscaled consumers on Kafka lag with KEDA, recovering from a **Z**x load spike in **N** seconds
- Verified zero message loss across pod and broker failures, with **M**-second recovery

## Schedule

Assumes about 4 weeks of break. With less, Phases 1, 2, 4, and 5 are the core project.

| Week | Focus |
| --- | --- |
| Before break | Phase 0 tutorials |
| Week 1 | Phase 1 (local pipeline) and start Phase 2 |
| Week 2 | Finish Phase 2 (on Kubernetes) and Phase 3 (alerts) |
| Week 3 | Phase 4 (autoscaling) and Phase 5 (failure testing) |
| Week 4 | Phase 6 (metrics, Grafana, README) and buffer |

## Stack

- Language: Python with `confluent-kafka` to start; Rust consumer later for a performance comparison
- Kafka on Kubernetes: Strimzi operator
- Local cluster: kind
- Storage: Postgres for results, Parquet on MinIO for raw metrics; batch: Spark via the Spark Operator
- Autoscaling: KEDA
- Metrics: Prometheus and Grafana

## Stretch goals

- Rewrite the consumer in Rust (rdkafka, tokio) and benchmark throughput, p99 latency, and memory against Python
  - Read first: [The Rust Book](https://doc.rust-lang.org/book/) · [Tokio tutorial](https://tokio.rs/tokio/tutorial) · [rdkafka crate](https://docs.rs/rdkafka)
- Upgrade the Parquet data lake to Apache Iceberg
- Exactly-once processing with Kafka transactions
- Deploy to a cloud cluster (EKS) for a real multi-node test (costs money; tear down right after)
