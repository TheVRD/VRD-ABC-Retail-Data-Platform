# Azure Data Factory — V1

This directory contains the Version 1 snapshot of the Azure Data Factory orchestration used by the ABC Retail Data Platform.

## Pipeline

`vrd_abc_retail_pipeline`

Flow:

```text
Bronze_Processing
        |
        v
Silver_Processing
        |
        v
Gold_Processing
```

Each Databricks activity receives the ADF pipeline parameter `processing_date` and passes it to the Databricks notebook as a base parameter.

## Retry configuration

Each Databricks notebook activity is configured with:

- Retry: 2
- Retry interval: 60 seconds
- Timeout: 12 hours

## Version 1 scope

V1 represents the working batch-processing implementation. The ADF activities currently point to the original Databricks workspace notebooks.

Git/CI-CD integration is intentionally left as a later enhancement.

## Security

No Databricks token, storage-account key, password, or other secret value is included.

The Databricks user email has been replaced with:

`<DATABRICKS_USER_EMAIL>`

because this repository is public.
