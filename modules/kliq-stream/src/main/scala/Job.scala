package kliq

import org.apache.spark.SparkContext
import org.apache.spark.sql._
import org.apache.spark.sql.{functions => F}
import org.apache.spark.sql.streaming.{DataStreamWriter, Trigger}

case class StreamJob(
    kafkaProps: KafkaProperties,
    hadoopProps: HadoopProperties
) {
  def run(implicit spark: SparkSession, sc: SparkContext): Unit = {
    import spark.implicits._

    val inputDf = spark.readStream
      .format("kafka")
      .option(
        "kafka.bootstrap.servers",
        kafkaProps.bootstrapServers
      )
      .option("subscribe", kafkaProps.topic)
      .load()

    val transformedDf = inputDf
      .selectExpr(
        "cast(value as string)"
      )
      .select(
        F.from_json($"value", EventSchema()).as("value")
      )
      .select("value.*")

    val writer = transformedDf.writeStream
      .format("json")
      .outputMode("append")
      .trigger(Trigger.ProcessingTime("10 seconds"))
      .option("maxRecordsPerFile", "100000")
      .option("checkpointLocation", s"${hadoopProps.uri}/checkpoint")
      .option("path", s"${hadoopProps.uri}/${hadoopProps.dataDir}")

    val streamingQuery = writer.start()
    streamingQuery.awaitTermination()

    streamingQuery.stop()
  }
}
