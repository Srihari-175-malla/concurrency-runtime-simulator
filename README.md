# Deterministic Execution & Concurrency Simulator (DECS)

## Overview
DECS is a deterministic execution environment designed for testing concurrent systems, asynchronous task queues, and network protocols under controlled pseudo-random seeds.

## Features
- **Virtual Clock**: Advances execution time deterministically.
- **Fault Injector**: Simulates packet drops, latency jitter, and out-of-order delivery.
- **Deterministic Replay**: Ensures 100% reproducible test traces for debugging race conditions.

## Usage
```bash
python -m unittest discover -s tests
```
