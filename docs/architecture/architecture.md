# Architecture

## High-Level Architecture

```text
                    +-------------------------+
                    | Python Test Data        |
                    | Generator               |
                    +------------+------------+
                                 |
                                 v
                    +-------------------------+
                    | ADLS Gen2               |
                    | Landing                 |
                    +------------+------------+
                                 |
                                 v
                    +-------------------------+
                    | Databricks Bronze       |
                    | Raw + operational meta  |
                    +------------+------------+
                                 |
                                 v
                    +-------------------------+
                    | Validation              |
                    +---------+-------+-------+
                              |       |
                            valid   invalid
                              |       |
                              v       v
                         +--------+ +-----------+
                         | Silver | | Quarantine|
                         +---+----+ +-----------+
                             |
                             v
                         +--------+
                         |  Gold  |
                         +--------+

             +-----------------------------------+
             | Azure Data Factory                 |
             | Scheduling / dependencies / retry |
             +-----------------------------------+
```

## Responsibility Split

### Azure Data Factory

ADF is responsible for:

- Scheduling
- Pipeline parameters
- Activity dependencies
- Retry configuration
- Pipeline monitoring
- Coarse-grained orchestration

### Azure Databricks

Databricks is responsible for:

- Reading/writing Delta
- Validation
- Transformations
- Incremental processing
- Aggregations
- Metadata processing
- Spark execution

### ADLS Gen2

ADLS provides durable cloud storage for the landing/data layers.

## Medallion Responsibilities

### Bronze

Preserve source-oriented data plus ingestion metadata.

### Silver

Provide validated, standardized, business-ready transactional data.

### Gold

Provide aggregated datasets optimized for analytical consumption.
