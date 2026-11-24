"""Metrics consumer.

Reads from the Kafka `metrics` topic as part of a consumer group, computes
rolling statistics per host and per cluster, and writes results to Postgres.

Later phases add:
- Anomaly detection, publishing flagged readings to the `alerts` topic (Phase 3)
- Careful offset commits so no messages are lost when a pod dies (Phase 5)
- Metrics exposed for Prometheus: throughput, end-to-end latency (Phase 6)

Scaled automatically by KEDA based on consumer lag (Phase 4).

To be implemented in Phase 1.
"""
