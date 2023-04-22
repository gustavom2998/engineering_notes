# The Executor

## The Default Executor

Executors are important to understand because they define how the task will be executed in the airflow instance. The local executor is good for executing local tasks in parallel, the kubernetes for running task in separate Kubernetes pods. 

Behind the executor, there is always a queue. This is where tasks are pushed and pulled by the workers.  Once the tasks are in the queue, the executor defines which tasks will be executed. The default executor, also known as the sequential executor, is the one that comes configured with airflow. 

The reason the default executor can't execute multiple tasks in parallel is because SQLite doesn't allow multiple read/writes in parallel. 

The sequential executor is useful for debugging tasks, or experimenting with airflow. Otherwise, it should basically never be used. 

To configure the executor the following commands can be used:

```bash
docker ps
docker exec -it {scheduler_id} /bin/bash
// Here we are inside the container
grep executor airflow.cfg // This by default will print default_executor

grep sql_alchemy_conn airflow.cfg // This will print sqlite://...

```

## Concurrency Parameters

When dealing with concurrency and wanting to execute parallel tasks in airflow, the are some very important parameters. These are:

- Global Airflow Instance Paramaters
    - parallelism: Maximum number of airflow tasks that can be executed in parallel for the entire airflow instance (32 by default).
    - dag_concurrency: Maximum number of tasks for a given DAG that can be executed in parallel across all of the DAG runs (16 by default).
    - max_active_runs_per_dag: Number of DAG runs that can happen at the same time for a give DAG (16 by default).
- Local DAG parameters
    - max_active_runs: Limit the number of DAG runs for a given DAG in parallel.
    - concurrency: Limit the number of tasks that can be executed in parallel for a specific DAG.

## Scalability

To run airflow in production, generally we want more than one task in parallel. The local executor allows us to run multiple tasks in parallel on one machine. Each task becomes a sub-process. It's extremely simple, and only requires the database to be configured with POSTGRES. 

## Scability in the cloud

At one point, in a local instance, we reach a limit. To execute as many tasks as we want, we can use the celery executor. For that, we can use a celery cluster. 

Celery is a distributed task queue allowing us to distribute tasks across multiple machines, so tasks aren't executed in a single machine. 

For example, we might have 5 nodes available. The web server and scheduler can run a single machine. On the second node we can the the metadata database. With the celery executor, we can set up the queue with RabbitMQ or REDIS (where tasks are pushed or pulled to). This can also be set up on the second node.

On the three remaining nodes, we can specify that they are celery workers for executing tasks. We can add as many workers as we want. With more machines, we need to maintain Airflow on the machines and we need to match the DAG dependencies. 

# Resources