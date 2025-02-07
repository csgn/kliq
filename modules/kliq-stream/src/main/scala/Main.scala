package kliq

import scala.util.Properties.envOrNone

import org.apache.spark.sql.{SparkSession}

object Main extends App {
  implicit val spark = SparkSession.builder
    .appName("kliq-stream")
    .master("local[*]")
    .getOrCreate()

  implicit val sc = spark.sparkContext

  val kafkaProps = KafkaProperties(
    bootstrapServers = envOrNone("KLIQ_STREAM__KLIQ_KAFKA__ADDR").get,
    topic = envOrNone("KLIQ_STREAM__KLIQ_KAFKA__TOPIC").get
  )

  val hadoopProps = HadoopProperties(
    uri = envOrNone("KLIQ_STREAM__KLIQ_HADOOP__URI").get,
    dataDir = envOrNone("KLIQ_STREAM__KLIQ_HADOOP__DATA_RAW_DIR").get
  )

  try {
    StreamJob(kafkaProps, hadoopProps).run
  } catch {
    case e: Exception => {
      println(("########### SKIP ERRORS", e))
    }
  }

  spark.stop()
}
