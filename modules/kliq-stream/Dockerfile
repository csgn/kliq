ARG JOB_NAME=app
ARG SPARK_VERSION=3.4.4
ARG SCALA_VERSION=2.12
ARG SBT_VERSION=1.10.2
ARG BASE_URL=https://dlcdn.apache.org/spark/spark-${SPARK_VERSION}
ARG SPARK_TGZ_URL=${BASE_URL}/spark-${SPARK_VERSION}-bin-hadoop3.tgz
ARG SBT_TGZ_URL=https://github.com/sbt/sbt/releases/download/v${SBT_VERSION}/sbt-${SBT_VERSION}.tgz
ARG SPARK_HOME=/opt/spark
ARG SBT_HOME=/opt/sbt
ARG TARGET_JAR=/app/target/scala-${SCALA_VERSION}/${JOB_NAME}_${SCALA_VERSION}-0.1.0-alpha.1.jar

# Stage 1
FROM eclipse-temurin:11-alpine AS builder
ARG SPARK_VERSION
ARG SPARK_TGZ_URL
ARG SBT_TGZ_URL
ARG SPARK_HOME
ARG SBT_HOME

ENV SPARK_HOME=${SPARK_HOME}
ENV SBT_HOME=${SBT_HOME}
ENV PATH=${SPARK_HOME}/bin:${SBT_HOME}/bin:$PATH

RUN apk --update add wget tar bash

RUN export SPARK_TMP="$(mktemp -d)" \
    && cd ${SPARK_TMP} \
    && wget -nv -O spark.tgz "${SPARK_TGZ_URL}" \
    && tar -xf spark.tgz \
    && mv spark-${SPARK_VERSION}-bin-hadoop3 ${SPARK_HOME} \
    && ln -s ${SPARK_HOME}/bin/spark-submit /usr/bin/spark-submit


RUN export SBT_TMP="$(mktemp -d)" \
    && cd ${SBT_TMP} \
    && wget -nv -O sbt.tgz "${SBT_TGZ_URL}" \
    && tar -xf sbt.tgz \
    && mv sbt ${SBT_HOME} \
    && ln -s ${SBT_HOME}/bin/sbt /usr/bin/sbt


# Stage 2
FROM eclipse-temurin:11-alpine
ARG SBT_HOME
ARG SPARK_HOME
ARG TARGET_JAR
ARG SCALA_VERSION
ARG SPARK_VERSION

ENV SPARK_HOME=${SPARK_HOME}    
ENV SBT_HOME=${SBT_HOME}
ENV SCALA_VERSION=${SCALA_VERSION}
ENV SPARK_VERSION=${SPARK_VERSION}
ENV TARGET_JAR=${TARGET_JAR}
ENV PATH=${SPARK_HOME}/bin:${SBT_HOME}/bin:$PATH

COPY --from=builder ${SBT_HOME} ${SBT_HOME}
COPY --from=builder ${SPARK_HOME} ${SPARK_HOME}

RUN apk --update add bash

WORKDIR /app
COPY . .
RUN sbt clean package
EXPOSE 4040
CMD ["sh", "-c", "spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_${SCALA_VERSION}:${SPARK_VERSION} --deploy-mode client ${TARGET_JAR}"]