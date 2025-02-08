# Overview
There are few jobs to perform ETL process and we are using `Apache Airflow` for scheduling them.

# Stages
![kliq-batch-stages-diagram.png](/docs/resources/kliq-batch-stages-diagram.png)

[Edit diagram](kliq-batch-stages-diagram.mmd)


| Name                | Description                                                                                                                                                                    |
| ---                 | --                                                                                                                                                                             |
| prepare_raw_events  | Move all `raw events` from `raw/` directory into `stage/` directory for prepare the data in order to process.                                                                  |
| process_raw_events  | Reads the `staged events` from `stage/` directory and performs data transformations and then writes the `transformed events` into `final/` directory.                          |
| archive_raw_events  | After the processing, move all `staged events` from `stage/` directory into `archive/` directory. It performs backing up the data for any fault or reprocessing circumstances. |

# Ports
| Port       | Description               |
| ---        | ---                       |
| 40042:8080 | Access to Airflow Web UI. |

# Changelogs
- [v0.1.0-alpha.1](/modules/kliq-batch/CHANGELOG.md#v010-alpha1)