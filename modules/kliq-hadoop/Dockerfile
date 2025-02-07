ARG HADOOP_HOME=/opt/hadoop
ARG HADOOP_VERSION=3.4.0

# Stage 1
FROM eclipse-temurin:11-jdk-focal AS builder
ARG HADOOP_HOME
ARG HADOOP_VERSION
ARG HADOOP_TGZ_URL=https://dlcdn.apache.org/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz

RUN apt-get update -y \
    && export DEBIAN_FRONTEND=noninteractive && apt-get install -y --no-install-recommends wget \
    && apt-get clean

ENV HADOOP_HOME=${HADOOP_HOME}

RUN mkdir -p ${HADOOP_HOME} \
    && wget -nv -O /tmp/hadoop.tar.gz "${HADOOP_TGZ_URL}" \
    && tar -xf /tmp/hadoop.tar.gz -C ${HADOOP_HOME} --strip-components 1 \
    && rm /tmp/hadoop.tar.gz \
    && rm -rf ${HADOOP_HOME}/share/doc


# Stage 2
FROM eclipse-temurin:11-jdk-focal
ARG HADOOP_HOME
ARG HADOOP_VERSION

RUN apt-get update -y \
    && export DEBIAN_FRONTEND=noninteractive && apt-get install -y --no-install-recommends sudo ssh \
    && apt-get clean

COPY conf/ssh_config /etc/ssh/ssh_config
RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa \
    && cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys \
    && chmod 0600 ~/.ssh/authorized_keys

ENV HADOOP_HOME=${HADOOP_HOME}
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root
ENV PATH=$PATH:${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin
ENV YARNSTART=0

COPY --from=builder ${HADOOP_HOME} ${HADOOP_HOME}

RUN echo "export JAVA_HOME=/opt/java/openjdk/" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

COPY conf/core-site.xml ${HADOOP_HOME}/etc/hadoop/
COPY conf/hdfs-site.xml ${HADOOP_HOME}/etc/hadoop/
COPY conf/yarn-site.xml ${HADOOP_HOME}/etc/hadoop/

COPY scripts/entrypoint.sh ${HADOOP_HOME}/etc/hadoop/
COPY scripts/healthcheck.sh ${HADOOP_HOME}/etc/hadoop/
WORKDIR /app

RUN sudo ln -s ${HADOOP_HOME}/etc/hadoop/entrypoint.sh /app/entrypoint.sh
RUN sudo ln -s ${HADOOP_HOME}/etc/hadoop/healthcheck.sh /app/healthcheck.sh

EXPOSE \
    # webui
    9870 \
    # namenode metadata service
    9000 \
    # ssh
    22

ENTRYPOINT [ "/app/entrypoint.sh" ]
