import sys
from typing import Iterator, Tuple

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import pyspark.sql.functions as F


def is_df_empty(df) -> bool:
    return not df.head(1)


class Job:
    def __init__(
        self,
        spark: SparkSession,
    ):
        self.spark = spark

    def read(self, *, src_dir: str, schema: StructType, **kwargs) -> DataFrame:
        if schema is None:
            raise ValueError("A schema must be provided for reading data.")

        return self.spark.read.json(str(src_dir), schema=schema, **kwargs)

    def transform(self, *, input_df: DataFrame) -> Iterator[Tuple[str, DataFrame]]:
        if is_df_empty(input_df):
            return

        event_channels = input_df.select("channel").distinct().rdd.flatMap(list).collect()
        for event_channel in event_channels:
            yield (event_channel, input_df.where(F.expr("channel") == event_channel))

    def write(
        self,
        *,
        result_df: DataFrame,
        dest_dir: str,
        **kwargs,
    ) -> None:
        if is_df_empty(result_df):
            return

        return result_df.write.save(
            str(dest_dir),
            format="json",
            mode="append",
            **kwargs,
        )

    def run(self, *, src_dir: str, dest_dir: str, schema: StructType):
        input_df = self.read(src_dir=src_dir, schema=schema)
        if is_df_empty(input_df):
            return

        for event_channel, result_df in self.transform(input_df=input_df):
            if not is_df_empty(result_df):
                final_dest_dir = dest_dir + "/" + event_channel
                self.write(result_df=result_df, dest_dir=final_dest_dir)


def main(args: list[str]) -> None:
    if len(args) != 4:
        print(
            "Usage: process_raw_event.py <hadoop-uri> <hadoop-src-dir> <hadoop-dest-dir>\n"
        )
        return

    hadoop_uri = args[1]
    hadoop_src_dir = hadoop_uri + "/" + args[2]
    hadoop_dest_dir = hadoop_uri + "/" + args[3]
    schema = StructType(
        [
            StructField("id", StringType(), False),
            StructField("timestamp", StringType(), False),
            StructField("channel", StringType(), False),
            StructField("ipaddress", StringType(), False),
        ]
    )

    spark = (
        SparkSession.builder.master("local").appName("process_raw_event").getOrCreate()
    )

    job = Job(spark)
    job.run(src_dir=hadoop_src_dir, dest_dir=hadoop_dest_dir, schema=schema)


if __name__ == "__main__":
    sys.exit(main(sys.argv))