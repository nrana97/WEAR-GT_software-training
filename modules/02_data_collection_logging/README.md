# Level 2: Data collection and logging

**Status: stub. Not yet written.**

## Draft learning goals

- Capture streaming sensor data without dropping samples
- Timestamp and synchronize multiple streams
- Choose a file format and write sessions with metadata (subject, task, sensor placement, firmware version)
- Run basic data-quality checks automatically on every session

## Prerequisites

Level 1 (or its checkpoint).

## Checkpoint idea

Given two simulated sensor streams running at different rates with clock offset, write a logger that aligns them onto a common timeline and writes a session file with complete metadata.

## Open questions before writing this module

- Session file format and naming convention (see `capstone_pipeline/README.md`)
- Whether a sync library such as Lab Streaming Layer is worth adopting
- Human-subject data handling rules and any IRB requirements
