# kliq-stream

# Overview
The `kliq-stream` is a `Spark Structured Streaming` service that reads the raw events from `kliq-kafka`
and writes them into the `kliq-hadoop` service as a JSON file.

# Ports
| Port       | Description             |
| ---        | ---                     |
| 30040:4040 | Access to Spark Web UI. |

# Changelogs
- [v0.1.0-alpha.1](/modules/kliq-stream/CHANGELOG.md#v010-alpha1)