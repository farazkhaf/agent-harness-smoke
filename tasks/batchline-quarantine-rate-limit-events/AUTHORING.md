# Task design — agent-harness-smoke/batchline-quarantine-rate-limit-events 0.1.1

## Purpose

This task scans a deterministic JSONL incident archive and writes the IDs of events matching an explicit worker, event type, provider, and inclusive timestamp window.

The task does not require incident diagnosis or hidden target discovery. The interaction pressure comes from inspecting and filtering a multi-megabyte line-oriented artifact while preserving the source archive.

## Interaction focus

Primary interaction family: large line-oriented inspection/filtering.

The task may be solved with shell filters, Python, repository helpers, chunked reads, or another mechanism. The verifier does not prescribe the inspection route.

## Contract boundary

The verifier checks that:

- `operations/quarantine-events.txt` contains exactly the ten matching event IDs;
- IDs are written one per line in chronological order;
- the incident archive is unchanged.

Additional repository changes are not prohibited unless they violate the stated contract.

## Version note

Version 0.1.1 keeps the task instruction unchanged and computes expected IDs with verifier-owned JSONL parsing.
