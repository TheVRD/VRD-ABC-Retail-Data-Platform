# Spark and Delta Optimization Experiments

This document summarizes V1 learning/benchmark experiments. These experiments are separate from the core production-style batch path.

## OPTIMIZE

Delta table compaction was tested using `OPTIMIZE`.

A Silver test table was reduced from multiple small files to a smaller compacted file set.

The experiment demonstrated the operational purpose of compaction: reducing small-file overhead and improving storage layout.

## Z-ORDER

Z-ORDER was tested on a separate isolated dataset.

The experiment demonstrated that Z-ORDER is a data-layout optimization and is distinct from liquid clustering.

Because the benchmark dataset was relatively small and compaction occurred during the test, the observed runtime differences were not treated as a reliable production performance claim.

## Delta Lifecycle

The project also explored:

- Time travel
- Deletion vectors
- `REORG APPLY PURGE`
- `VACUUM DRY RUN`

Destructive retention settings were not used on the production-style Silver dataset.

## Liquid Clustering

Liquid clustering was evaluated conceptually, but the actual V1 Silver table was intentionally not converted to AUTO liquid clustering.

## Principle

Optimization should be driven by:

- Data volume
- Query patterns
- File sizes
- Selectivity
- Write/read workload
- Measured evidence

rather than applying optimization features automatically.
