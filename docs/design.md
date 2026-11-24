# Design Doc: Telemetry Pipeline

Status: draft. Fill in each section as you learn the concept behind it.

## 1. Goals

- Ingest metrics from N simulated hosts in real time
- Detect anomalies (CPU, memory, latency, errors, silent hosts) within a few seconds
- Scale consumers automatically when they fall behind
- Lose zero messages when pods or brokers fail

Non-goals: production security hardening, multi-region deployment.

## 2. Architecture

Producers, Kafka, consumers, Postgres, alert service, and monitoring, all on one kind cluster. See the diagram in the README.

TODO: explain why each component exists and what would break without it.

## 3. Data model

Message schema: see README.

TODO:
- Why JSON vs. Avro/Protobuf, and what a schema registry would add
- Postgres tables for results and alerts

## 4. Topics, keys, and partitions

TODO:
- Why `host_id` is the message key (ordering per host)
- How many partitions, and how that limits consumer parallelism
- Topic retention settings

## 5. Delivery guarantees

TODO:
- Producer `acks` setting and idempotence
- When consumers commit offsets (before or after writing to Postgres) and what each choice risks
- At-least-once vs. exactly-once, and how duplicates are handled

## 6. Scaling

TODO:
- KEDA scaling on consumer lag: thresholds, min and max replicas
- Why consumers can't scale past the partition count

## 7. Failure scenarios

| Failure | Expected behavior | How to verify | Result |
| --- | --- | --- | --- |
| Consumer pod killed | Group rebalances, another consumer takes over its partitions | Count messages sent vs. stored | TBD |
| Kafka broker killed | Replicas keep the topic available | Producer keeps writing, no errors | TBD |
| Postgres restarts | Consumers retry, no lost writes | Count messages sent vs. stored | TBD |
| Producer burst (10x load) | Lag grows, KEDA adds consumers, lag recovers | Lag graph in Grafana | TBD |

## 8. Observability

TODO: which metrics Prometheus scrapes (throughput, consumer lag, end-to-end latency) and what each dashboard shows.

## 9. Open questions

- TODO: add questions as they come up while building
