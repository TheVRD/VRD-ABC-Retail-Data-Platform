# V1 Scope

## Status

**Complete**

V1 establishes the working batch retail data platform.

## Included

- Python data generation
- ADLS Gen2 landing
- Databricks Bronze
- Validation
- Quarantine
- Silver
- Gold
- Delta Lake
- Metadata/audit logging
- Incremental file processing
- Idempotency
- ADF orchestration
- Scheduled execution
- Spark/Delta experiments
- Git/GitHub version control

## Explicitly Deferred

The following are not claimed as V1 production capabilities:

- REST API ingestion
- Streaming ingestion
- CI/CD deployment automation
- Automated environment promotion
- Fully automated Git-to-ADF deployment

These are future milestones.

## Next Milestones

### V2 — API ingestion

Introduce a realistic external API source and design an ingestion pattern that handles:

- authentication
- pagination
- retries
- rate limits
- incremental extraction
- raw response preservation
- API failure handling

### V3 — Streaming

Introduce a streaming source and implement:

- Structured Streaming
- checkpoints
- incremental processing
- late-arriving data considerations
- exactly-once/idempotent sink design

### V4 — CI/CD

Improve deployment with:

- Git-based promotion
- environment separation
- automated validation
- deployment automation
- controlled production release
