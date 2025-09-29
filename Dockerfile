# infra/docker/spark.Dockerfile
FROM bitnami/spark:3.5.1
USER root
RUN pip install delta-spark==3.2.0 great-expectations==0.18.12
USER 1001