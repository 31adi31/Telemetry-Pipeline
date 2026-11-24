"""Metrics producer.

Simulates N servers across a few clusters. Each simulated host sends a metrics
reading (CPU, memory, disk and network I/O, p99 latency, error rate) to the
Kafka `metrics` topic at a configurable rate, keyed by `host_id` so each host's
readings stay ordered within one partition.

Later phases add:
- Daily load patterns so traffic rises and falls realistically
- Injected anomalies: CPU pinned at 100%, memory leaks, cluster-wide latency
  and error spikes, and hosts going silent
- A burst mode for load testing autoscaling

To be implemented in Phase 1.
"""
