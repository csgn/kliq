package kliq

import org.apache.spark.sql.types._

object EventSchema {
  def apply() = {
    StructType(
      Array(
        StructField("id", StringType, nullable = false),
        StructField("timestamp", StringType, nullable = false),
        StructField("channel", StringType, nullable = false),
        StructField("ipaddress", StringType, nullable = false),
      )
    )
  }
}
