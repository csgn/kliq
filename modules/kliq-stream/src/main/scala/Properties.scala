package kliq

case class KafkaProperties(
    bootstrapServers: String,
    topic: String
) {
  require(bootstrapServers != "")
  require(topic != "")
}

case class HadoopProperties(
    uri: String,
    dataDir: String
) {
  require(uri != "")
  require(dataDir != "")
}

