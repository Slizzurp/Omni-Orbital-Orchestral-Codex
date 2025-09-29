# pipelines/spark/batch/curate_evidence.py
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("s3oc-curation").getOrCreate()

tele = spark.read.format("delta").load("s3://codex/data/silver/telemetry")
artifacts = spark.read.format("delta").load("s3://codex/data/silver/artifacts")
links = spark.read.format("delta").load("s3://codex/data/silver/links")  # relationships

# Example: join by subject id, build evidence packs
evidence = (tele.alias("t")
  .join(links.alias("l"), F.col("t.subject.id")==F.col("l.asset_id"), "left")
  .join(artifacts.alias("a"), F.col("l.artifact_id")==F.col("a.id"), "left")
  .groupBy("t.subject.id")
  .agg(
    F.collect_list(F.struct("t.id","t.timestamp","t.measures","t.provenance")).alias("observations"),
    F.collect_set(F.struct("a.id","a.kind","a.uri","a.hash")).alias("artifacts")
  )
  .withColumn("evidence_id", F.sha2(F.concat_ws(":", F.col("t.subject.id"), F.current_timestamp()), 256))
  .withColumn("created_at", F.current_timestamp()))

evidence.write.format("delta").mode("overwrite").save("s3://codex/data/gold/evidence_packs/v1")