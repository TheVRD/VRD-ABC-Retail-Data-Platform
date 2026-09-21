# Metadata and Idempotency

## Problem

A batch pipeline must be safe to retry. Re-running a pipeline should not blindly duplicate already-processed source files.

## Processing Identity

The implementation uses:

```text
source_file_path + source_layer + target_layer + data_entity
```

as the logical processing context.

## Example

If Bronze contains:

```text
file_A
file_B
file_C
```

and metadata shows successful:

```text
file_A: bronze -> silver
file_B: bronze -> silver
```

then:

```text
Pending = file_C
```

Only `file_C` is processed.

## Processing Log

The data-processing log records:

- source file
- source layer
- target layer
- entity
- execution ID
- status
- timestamps
- rows processed
- error information
- pipeline
- environment

## Retry Semantics

Failed processing is retained as failed metadata.

A later successful retry creates a successful processing record.

This gives the pipeline an audit trail while allowing the pending-file calculation to consider successful processing separately from failed attempts.
