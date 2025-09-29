.PHONY: dev up test run-sim
dev:
\tuvicorn services.conductor.main:app --reload --port 8080

up:
\tdocker compose up -d

test:
\tpytest -q

run-sim:
\tpython tools/sim/signalgen.py | curl -s -X POST localhost:8083/ingest -H 'Content-Type: application/json' -d @-
spark-telemetry:
\tspark-submit --properties-file infra/spark/spark-defaults.conf pipelines/spark/streaming/telemetry_ingest.py

spark-curate:
\tspark-submit --properties-file infra/spark/spark-defaults.conf pipelines/spark/batch/curate_evidence.py