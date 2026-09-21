# Data Quality Design

Sales validation is rule-driven.

## Current Rules

### Required fields

Required columns are checked for null values.

### Primary-key uniqueness

`saleId` is treated as the sales record key.

### Positive numeric values

Relevant numeric fields are checked for valid positive values.

### Allowed payment modes

Payment mode values are checked against the configured allowed values.

## Processing Outcome

```text
                 Sales Input
                     |
                     v
                 Validation
                 /                      Valid       Invalid
                |            |
                v            v
             Silver      Quarantine
```

Invalid records are retained in the quarantine layer rather than silently discarded.

The validation framework is implemented as reusable validation rules so additional rules can be introduced without rewriting the complete pipeline.
