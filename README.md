# spark_flow

# Airflow DAG flow

```mermaid
graph TD;
    start-->re_partition;
    re_partition-->join_df;
    join_df-->agg;
    agg-->task_end;
```
