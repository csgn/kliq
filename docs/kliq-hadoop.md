# kliq-hadoop

# Overview
The kliq-hadoop service is an HDFS cluster and storing all events (raw, archive, processed, etc.) as a JSON file in directories. Directory hierarchy as follows table:

```
data/
  raw/
  stage/
  archive/
  final/
tmp/
users/
checkpoint/ # kliq-stream's checkpoint path
```

# Ports
| Port      | Description                                                   |
| ---       | ---                                                           |
| 9870:9870 | Access to cluster's ui.                                       |
| 9000:9000 | Access to Namenode.                                           |
| 9864:9864 | Access to Datanodes in order to look up or download the data. |


# Changelogs
- [v0.1.0-alpha.1](/modules/kliq-hadoop/CHANGELOG.md#v010-alpha1)