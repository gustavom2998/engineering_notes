# Airflow Essentials

## ETL Problem

We start by exploring a very simple ETL data pipeline:

Extracting → Transforming → Loading

**Extracting:** Loads data from an API. What happens if the data is not available?

**Transforming:** Transforming data with DBT or Spark. What happens if DBT or Spark job fails? What to do.

**Loading:** Store it in a database. If the data base is not reachable, we can't store the data. Maybe retry?

- The lesson is that any step of this data pipeline can fail.
- In practice, most pipelines are much more and complex, and there are multiple data pipelines that must be monitored.
- Without the right tool, this becomes a nightmare.
- CRON is often used to handle data pipelines. But it is extremely limited.
    - Can't handle complex dependencies between tasks
    - Can't monitor tasks automatically
    - Can't retry failed tasks
    - No notification for fails
    - No interface to manage data pipelines
- Airflow is the solution to CRON
    - Perfect tool to create, monitor and manage data pipelines.

## What is Airflow?

**Apache Airflow** is an open source platform to programmatically author, schedule and monitor workflows. It's an orchestrator for creating dynamic data pipelines and executing tasks in the right order, in the right way, in the right time. 

We can produce statistics based on user data. We create a pipeline with two tasks. 

The first processes the data. This can trigger a Spark job from Airflow.

Then the statistics can be stored in a database using a task from Airflow. 

Notice that these tasks interact with other tools such as Spark, POSTGRES, MySQL, DBT, ElasticSearch, etc. Airflow integrates with all these tasks. 

If any failure happens in the process, there will be a warning.

## Benefits

The benefits of using airflow are:

- **Dynamic Pipelines:** Pipelines are coded in Python. Anything you can do with Python, you can do for a data pipeline.
- **Scalable:** You can execute as many tasks as you want. If you have a Kubernetes cluster, you can execute a task on it. You can choose the Kubernetes executor to this. If you have a Celery cluster, you can use the Celery executor. Independent of the architecture, you have a way to execute the tasks.
- **Interactive:** Highly interactive with multiple methods of interaction. Visual User interface; CLI; and an API for calling an execution from a front-end for example.
- **Extensible:** It can be customized as much as needed. If there is a new tool you want to add, you can write your own plugin to interact with the tool, you can change the user interface, you can change the way tasks are executed, you want to add new functionalities, you can customize everything.

## What Airflow isn't

- Not a data processing framework. It isn't Spark. Don't process large amounts of data WITH Airflow. Make Airflow orchestrate the mechanism that processes this data. Make it call a Spark Job that processes this data.
- Not a streaming solution. Don't try to trick the scheduling interval to trigger the data pipeline every second. It won't work.

## Airflow Core Components

By default airflow runs three core components. 

### Web Server

The web server is a Flask Server with Gunicorn serving the user interface.

Without it, we can't access the user interface and cant monitor and manage our data pipelines.

#### Scheduler

The heart of airflow. Without it, we can't schedule and trigger tasks. We can have multiple schedulers running at the same time, so if one goes down, another can be used.

## Metadata Database

Stores data related to users, jobs, connections, any airflow data is stored into the metadata database. 

Any database that is compatible with SQL-Alchemy can be used for Airflow such as: POSTGRES, MySQL, Oracle, SQLite, MongoDB. 

There are also two additional components that run behind the scene:

### Executor

Defines how tasks are going to be executed by Airflow on which system. There is queue behind each executor to  define the order of execution.

If you have a Kubernetes Cluster, and you want to execute the task on Kubernetes, you use the Kubernetes executor. 

For a Celery cluster, you use the Celery executor and so on. 

If you want to execute multiple tasks at once, you can use the local executor. 

By default airflow uses the sequential executor, where tasks are executed one after the other. You can also 

### Worker

Defines where tasks are going to be executed. It's a process or subprocess where the task is executed. If using Kubernetes, the worker is a Pod where the task is executed. 

## Integrating Core Components - 2 Common Architectures

### Single Node Architecture

Available out of the box. All the components of Airflow run on the same machine. This machine is called a node. The basic components are the Web Server, the scheduler, the metastore and the executor. 

The basic process is:

1. The **web server** interacts with the **metastore** database, getting the status of tasks, users, permissions, all the data that can be seen from the web server.
2. The **scheduler** then checks if a task is ready to be scheduled, it updates the task status in the **metastore**. Then a task instance is created and sent from the **scheduler** to the **executor** queue. The task is then ready to be fetched by a **worker** and executed.
3. The **executor** interacts with the **metastore** in order to update the task status as soon as the task is done.

An observation is that all components interact with the metastore. Besides that, the scheduler interacts with the executor. No other interactions occur.

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/fundamentals_1.png?raw=true)

### Multi nodes architecture (Celery)

If you want to start scaling airflow and execute as many tasks as you want, we need a new architecture. Assuming a celery cluster, we typically have multi nodes. With celery, the queue is external to the executor. The queue must be managed by Redis or RabbitMQ. The web server, scheduler and executor are also separate. The workers are then distributed across separate nodes.

The process works like this:

1. The web server interacts with the metastore
2. The scheduler interacts with the metastore and the executor. Once the task is ready to be scheduled, it is sent to the executor. 
3. The executor sends the task into the queue.
4. The works then interact with the queue and pull workloads to execute.

This architecture is extremely scalable since workers can be easily added as necessary. 

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/fundamentals_2.png?raw=true)

## Core concepts

The three core concepts are DAGs, dependencies and Workflow.

### DAGs

A DAG is basically a data pipeline. It stands for Directed Acyclic Graph. This means that:

- A DAG contains nodes and is connected by arrows.
- These arrows contain a direction.
- The graph cannot have any cycles/loops.
- It's cyclical since it must finish at some time.

**Operator:** A node represents a operator. It's a task in the DAG. It's an object around the task we want to executed. There are three types of operators:

- Action Operators: Allow us to execute something in the data pipeline. It can be used to execute a Python command using the Python operator, or a bash command using the Bash Operator, and so.
- Transfer Operators: Allow us to transfer data from a source to a destination. For example, there is a transfer operator for transferring data from MySQL to PrestoDB.
- Sensor Operators: Needed when we need to wait for something to happen to trigger a task. For example, we can wait for a file to be created in a directory, and then trigger the task to process the file.

**Task:** Once an operator is instanced inside a DAG, it becomes a task. 

**Task Instance Object:** A task ready to be scheduled, it becomes a task instance object. It represents a specific run of a task. It's a function of a DAG + Task + Point in time.

### Depedencies

By specifying relationships in the DAG between tasks, we have dependencies. For example, for the following pipeline:

Operator A → Operator B → Operator C

We want A to execute first, then B, then C. To define dependencies in airflow there are two ways:

- By function: set_upstream OR set_downstream functions
- Bitshift Operator: << (left bitshift) or >> (right bitshift)

### Workflow

A workflow is the combination of all concepts that have been explained. A DAG + Operator + Task is a workflow. 

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/fundamentals_3.png?raw=true)

## Task Lifecycle

In this topic, we explain what happens when a task is ready to be triggered in Airflow. Through out its lifecycle, a task begins with no status, then can proceed to have the status "scheduled", "queued", "running" and "success". 

In the node, we now include the Folder DAGs which contains the DAGs to be executed. Inside DAGs we define a Python file (for example, dag.py). This file will be parsed by both the web server and the scheduler. The web server parses DAGs every 30 seconds, while the scheduler parses new DAGs every 5 minutes, by default. 

Once the DAG has been parsed by the web server and the scheduler, if the DAG is ready to be triggered, the scheduler instances a DagRun Object and writes it to the Metastore. Initially, the task has no status. As soon as the task is ready to be triggered, the status is updated to the "Scheduled" value. 

Then the scheduler sends the task to the executor, and the task receives the status "Queued". Once this is updated, the task is ready to be given to a worker by the executed and receive the status "Running". Once the task is done, the status in the metastore is updated to "success" by the executor if everything happened correctly. If the work is marked as done and there are no more tasks marked as scheduled, the scheduler allows the web server to refresh the UI. 

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/fundamentals_4.png?raw=true)

## Extras and Providers

By default, Airflow only contains some basic functionalities, bringing only what we need to get started. If you want to integrate other tools, you must download other dependencies. Airflow 2 is delivered in multiple separate but connected packages. 

**Extra:** An extra is a big package responsible for installing all dependencies for the functionality that we want. It's like a provider with additional dependencies that are installed.

For example, the extra celery extends the core apache airflow is extended.

**Provider:** Allows us to add functionalities on top of airflow. It's completely separate from the Airflow core.  It can be updated without updating airflow. They allow us to add functionalities on top of Airflow.

**Extra vs Provider:**

Extra allows us to install a set of dependencies necessary for a feature.

If we only need some operators or hooks, we install a provider. 

## Resources

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.operators.python import PythonOperator # Operator for executing Python funcs
from airflow.utils.dates import days_ago
from datetime import timedelta

def do_nothing():
    return None

with DAG(dag_id = 'simple_dag',start_date =days_ago(1), schedule_interval = timedelta(hours=7)) as dag:

    task_1 = PythonOperator(task_id = 'task_1',python_callable=do_nothing)
    
    task_2 = DummyOperator(task_id = 'task_2')

    task_3 = DummyOperator(task_id = 'task_3')

    task_4 = DummyOperator(task_id = 'task_4')

    task_1 >> [task_2, task_3] >> task_4
```
