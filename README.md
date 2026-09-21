# ABC Retail Data Platform

An Azure-based retail data engineering platform built to demonstrate production-oriented batch data engineering patterns using **Azure Data Factory, Azure Databricks, ADLS Gen2, Delta Lake, PySpark, Python, and SQL**.

> **Version 1 — Batch Data Platform**
>
> V1 is the working batch-processing implementation. API ingestion, streaming, and CI/CD improvements are planned as subsequent iterations.

## 1. Project Overview

The platform processes retail sales data from an ADLS Gen2 landing zone through a Medallion Architecture:

```text
Python Test Data Generator
          |
          v
      ADLS Gen2
       Landing
          |
          v
       Bronze
          |
          v
     Validation
       /         Valid   Invalid
      |        |
      v        v
    Silver  Quarantine
      |
      v
      Gold
```

Azure Data Factory orchestrates the major processing stages:

```text
ADF
 |
 +--> Bronze Processing
          |
          v
     Silver Processing
          |
          v
      Gold Processing
```

Databricks owns data processing; ADF owns workflow orchestration, dependencies, parameters, retries, and scheduling.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Test-data generation and utility development |
| SQL | Data analysis, validation, and Delta/Spark SQL work |
| PySpark | Distributed transformations and data processing |
| Azure Data Lake Storage Gen2 | Landing/data storage |
| Azure Databricks | Data processing and Delta Lake |
| Delta Lake | ACID tables, history, time travel, optimization |
| Azure Data Factory | Pipeline orchestration and scheduling |
| Git/GitHub | Source control and project versioning |

## 3. Repository Structure

```text
VRD-ABC-Retail-Data-Platform/
|
+-- test_data_generator/
+-- databricks/
|   +-- bronze/
|   +-- config/
|   +-- gold/
|   +-- models/
|   +-- setup/
|   +-- silver/
|   +-- transformations/
|   +-- utils/
|   +-- validation/
|
+-- adf/
|   +-- pipelines/
|   +-- README.md
|
+-- docs/
|
+-- .gitignore
+-- README.md
```

## 4. Data Flow

### Landing

The Python test-data generator produces realistic clean and corrupted retail sales records.

V1 test generation includes:

- 200,000 clean records
- 210,000 corrupted records
- Customer and product master data
- Store master data
- Generated timestamps
- Configurable bad-data injection

### Bronze

Bronze ingests source data and adds operational metadata:

- `source_file_path`
- `ingestion_timestamp`
- `processing_date`
- `pipeline_name`

### Validation

Sales data is checked using configurable rules including:

- Required/not-null fields
- Primary-key uniqueness
- Positive numeric values
- Allowed payment modes

Invalid records are separated into quarantine.

### Silver

Silver contains validated and transformed sales data.

Transformations include:

- Trimming string columns
- Standardizing payment modes
- Standardizing descriptive text
- Recalculating total amount
- Incremental file processing

Silver is stored in Delta format.

### Gold

Gold contains analytical fact tables for:

- Daily sales
- Store sales
- City sales
- Product sales
- Category sales
- Payment-mode sales

## 5. Incremental Processing and Idempotency

The platform uses `source_file_path` as the source-file identity.

A generalized metadata table records transitions such as:

```text
landing -> bronze
bronze  -> silver
```

A file is considered successfully processed only when a successful transition exists for the relevant source layer, target layer, and entity.

Example:

```text
Bronze files:
A.csv
B.csv
C.csv

Successfully processed:
A.csv
B.csv

Pending:
C.csv
```

A subsequent run processes only `C.csv`.

## 6. Metadata and Audit Logging

The `metadata` schema contains operational logs.

### Pipeline execution log

Tracks:

- Execution ID
- Pipeline name
- Notebook
- Data entity
- Environment
- Processing date
- Start/end timestamps
- Status
- Rows processed
- Error message

### Data processing log

Tracks:

```text
source_file_path
source_layer
target_layer
data_entity
execution_id
processing_status
start_timestamp
end_timestamp
rows_processed
error_message
pipeline_name
environment
```

## 7. Error Handling

Pipeline statuses include:

```text
started
success
failed
```

Failed data-processing attempts are retained as failed metadata.

ADF activities use:

- Retry: 2
- Retry interval: 60 seconds
- Timeout: 12 hours

## 8. Azure Data Factory

V1 contains `vrd_abc_retail_pipeline`.

```text
Bronze_Processing
       |
       | Succeeded
       v
Silver_Processing
       |
       | Succeeded
       v
Gold_Processing
```

The pipeline accepts `processing_date` and passes it to each Databricks notebook.

The V1 ADF pipeline has been successfully executed through a scheduled trigger.

> The V1 ADF definition is preserved under `adf/`. Git-backed Databricks execution/CI-CD integration is intentionally a later enhancement.

## 9. Security

Secrets are not stored in source code.

The Databricks configuration retrieves the storage-account secret through a Databricks secret scope:

```python
dbutils.secrets.get(
    scope="abc-retail-secrets",
    key="storage-account-key"
)
```

The repository does not contain the actual secret value.

Generated test data is excluded from Git through `.gitignore`.

## 10. Delta Lake and Spark Engineering

V1 includes practical experiments covering:

- Delta table writes
- Delta table history
- Time travel
- Deletion vectors
- `OPTIMIZE`
- Z-ORDER experimentation
- `VACUUM DRY RUN`
- `REORG APPLY PURGE`
- Spark partitioning and transformation behavior
- Performance benchmarking

These experiments are kept separate from the core production-style V1 processing flow.

## 11. SCD Type 2

An isolated SCD Type 2 test was implemented for customer-style dimensional data.

Tests covered:

- Initial records
- New records
- Attribute changes
- Idempotent reruns
- Multiple changes
- NULL-to-value transitions
- Value-to-NULL transitions

SCD2 is not applied directly to transactional sales in V1.

## 12. Design Principles

The project emphasizes:

- Separation of orchestration and processing
- Configuration-driven processing
- Reusable utilities
- Data-quality validation
- Idempotency
- Auditability
- Secure secret handling
- Delta Lake
- Incremental processing
- Clear Bronze/Silver/Gold responsibilities
- Version control

## 13. Version 1 Scope

### Implemented

- Python test-data generator
- ADLS Gen2 landing
- Bronze ingestion
- Data validation
- Quarantine
- Silver transformations
- Incremental file processing
- Idempotency
- Metadata logging
- Gold aggregations
- Delta Lake
- Spark/Delta optimization experiments
- SCD2 isolated testing
- Azure Data Factory orchestration
- Scheduled batch execution
- Git/GitHub source control

### Planned

- REST API ingestion
- API-to-ADLS ingestion patterns
- Streaming ingestion
- Structured Streaming
- Incremental/event-driven processing
- CI/CD automation
- Environment promotion
- Production-oriented Git/ADF/Databricks deployment workflow

## 14. Interview Discussion Topics

1. Why Medallion Architecture?
2. Why Delta instead of CSV/Parquet for curated layers?
3. How is idempotency achieved?
4. Why use `source_file_path` as a processing key?
5. How are bad records quarantined?
6. How does ADF differ from Databricks?
7. How would you handle a failed Silver write?
8. How would the design change for API ingestion?
9. How would the design change for streaming?
10. How would you implement CI/CD?
11. When would you use SCD Type 2?
12. How would you optimize a growing Delta table?
13. How would you handle schema evolution?
14. How would you promote DEV to TEST/PROD?

## 15. V1 Status

**V1 batch platform: complete and working.**

The next development milestone is API ingestion, followed by streaming ingestion. Further ADF/Git integration and CI/CD hardening can be added without disrupting the V1 baseline.
