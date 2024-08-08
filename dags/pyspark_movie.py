from datetime import datetime, timedelta
from textwrap import dedent
from pprint import pprint

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

from airflow.operators.python import (
        PythonOperator, 
        BranchPythonOperator, 
        PythonVirtualenvOperator,

)

with DAG(
    'pyspark_movie',
    default_args={
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(seconds=3),
    },
    max_active_runs=1,
    max_active_tasks=3,
    description='processing pyspark for movie data',
    schedule="10 2 * * *",
    start_date=datetime(2015, 1, 1),
    end_date=datetime(2025, 3, 1),
    catchup=True,
    tags=['api', 'movie', 'amt', 'pyspark'],
) as dag:

    def re_partition(ds_nodash):
        # import PDM Package ...
        print("*" * 33)
        print(ds_nodash)
        print("*" * 33)


    re_task = PythonVirtualenvOperator(
        task_id='re.partition',
        python_callable=re_partition,
        system_site_packages=False,
        requirements=["git+https://github.com/dMario24/mov.git@0.3.3/url_param"],
    )

    join_df = BashOperator(
        task_id='join.df',
        bash_command='''
            echo "spark-submit....."
            echo "{{ds_nodash}}"
            '''
    )

    agg_df = BashOperator(
        task_id='agg.df',
        bash_command='''
            echo "spark-submit....."
            echo "{{ds_nodash}}"
            '''
    )
    
    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end')
    
    # flow
    start >> re_task >> join_df >> agg_df >> end
