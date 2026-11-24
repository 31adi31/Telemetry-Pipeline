"""Alert service.

Consumes the Kafka `alerts` topic and logs or stores each alert (CPU pinned,
memory leak, latency and error spikes, silent hosts) in Postgres.

To be implemented in Phase 3.
"""
