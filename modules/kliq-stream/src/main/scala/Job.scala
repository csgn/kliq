package kliq

import org.apache.spark.SparkContext
import org.apache.spark.sql._
import org.apache.spark.sql.{functions => F}
import org.apache.spark.sql.streaming.{
  DataStreamWriter,
  Trigger,
  StreamingQuery,
  StreamingQueryException
}

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

    var streamingQuery: StreamingQuery = null
    val max_retry = 10
    var retry_count = 0
    while (retry_count < max_retry) {
      streamingQuery = writer.start()

      try {
        retry_count = 0
        streamingQuery.awaitTermination()
      } catch {
        case e: StreamingQueryException => {
          println("Streaming Query Exception: " + e)
          retry_count += 1
        }
      }
    }

    streamingQuery.stop()
  }
}
