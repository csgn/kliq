package kliq

import org.apache.spark.sql.types._

object EventSchema {
  def apply() = {
    StructType(
      Array(
        StructField("tv001", StringType, nullable = false)
      )
    )
  }
}
