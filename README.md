# Kliq

# Overview
A service will collect user events and store the raw data on the 
```Apache Hadoop``` cluster, and **internal consumers** can access the cluster via
```Apache Spark```, ```Presto``` etc. to read processed data in order to use
it in their own business purposes.

# Purpose of Service
We are collecting user events for the reasons listed below:

1. Recommend better **product** or **content** to users based on their 
historical behaviour.
2. Creating **advertising campaigns** based on users' behaviour.
3. Understand how **different page layouts** or **contents** affect users'
behaviour.

# Architecture
![kliq_diagram](/docs/resources/kliq-diagram.png)

[Edit diagram](/docs/kliq-diagram.mmd)

# Usage

## Run the service
```sh
$ ENV=dev make up # will use "docker/env/dev" environment file
```

## Down the service
```sh
$ ENV=dev make down 
```

## Stop the service
```sh
$ ENV=dev make stop
```

## Show the summary
```sh
$ ENV=dev make summary
```

# Modules
| Service                               | Description                                                                       |                                             
| ------------------------------------- | ----------------------------------------------------------------------------------|
| [kliq-collect](/docs/kliq-collect.md) | Exposes an HTTP server to collect user events and sent them into the kafka topic. |
| [kliq-kafka](/docs/kliq-kafka.md)     | A message broker for events.                                                      |


# License
```
MIT License

Copyright (c) 2024 Sergen Çepoğlu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.```
