# Data Pipeline Design

## Processing Flow

```text
Landing -> Bronze -> Validation -> Silver -> Gold
                         |
                         v
                     Quarantine
```

The pipeline is parameterized by `processing_date`.

## Bronze

Bronze reads source CSV data and appends operational metadata.

Key metadata:

- `source_file_path`
- `ingestion_timestamp`
- `processing_date`
- `pipeline_name`

## Silver

Silver identifies pending Bronze files using the data-processing metadata table.

Only pending files are read from Bronze.

For each file:

1. Read the relevant Bronze records.
2. Validate the data.
3. Transform valid records.
4. Write valid records to Silver.
5. Write invalid records to Quarantine.
6. Record processing status.

## Gold

Gold reads Silver and produces business aggregates.

Current fact tables:

- `fact_daily_sales`
- `fact_store_sales`
- `fact_city_sales`
- `fact_product_sales`
- `fact_category_sales`
- `fact_payment_mode_sales`

Gold V1 uses overwrite semantics for the aggregate tables.

## Orchestration

ADF invokes coarse-grained Databricks entry notebooks:

```text
Bronze_Processing
      |
Silver_Processing
      |
Gold_Processing
```

This keeps workflow orchestration separate from Spark data-processing logic.
