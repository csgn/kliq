import os
from datetime import datetime, timedelta

from airflow.models.dag import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
from airflow.utils.dates import days_ago

with DAG(
    "kliq-batch",
    description="Batch process for raw events.",
    schedule=timedelta(minutes=1),
    start_date=days_ago(1),
    catchup=False,
) as dag:
    start = DummyOperator(
        task_id="start_task",
    )

    # if this task failed go end otherwise go t2
    t1 = BashOperator(
        task_id="move_raw_events_task",
        bash_command="/opt/airflow/jobs/bash/move_events.sh ${KLIQ_BATCH__KLIQ_HADOOP__URI}/${KLIQ_BATCH__KLIQ_HADOOP__DATA_RAW_DIR} ${KLIQ_BATCH__KLIQ_HADOOP__URI}/${KLIQ_BATCH__KLIQ_HADOOP__DATA_STAGE_DIR} ",
    )

    # run this task when t1 is succeed
    t2 = SparkSubmitOperator(
        task_id="process_raw_event_task",
        application="/opt/airflow/jobs/python/process_raw_event.py",
        application_args=[
            # --hadoop-uri
            os.getenv("KLIQ_BATCH__KLIQ_HADOOP__URI"),
            # --hadoop-src-dir
            os.getenv("KLIQ_BATCH__KLIQ_HADOOP__DATA_STAGE_DIR"),
            # --hadoop-dest-dir
            os.getenv("KLIQ_BATCH__KLIQ_HADOOP__DATA_FINAL_DIR"),
        ],
        env_vars={
            "HADOOP_CONF_DIR": "/opt/hadoop",
            "YARN_CONF_DIR": "/opt/hadoop",
        },
    )

    t3 = BashOperator(
        task_id="move_stage_events_task",
        bash_command="/opt/airflow/jobs/bash/move_events.sh ${KLIQ_BATCH__KLIQ_HADOOP__URI}/${KLIQ_BATCH__KLIQ_HADOOP__DATA_STAGE_DIR} ${KLIQ_BATCH__KLIQ_HADOOP__URI}/${KLIQ_BATCH__KLIQ_HADOOP__DATA_ARCHIVE_DIR} ",
    )

    end = DummyOperator(
        task_id="end_task",
        trigger_rule="one_failed",
    )

    start >> t1
    t1 >> t2
    t1 >> end

    t2 >> t3
    t2 >> end

    t3 >> end