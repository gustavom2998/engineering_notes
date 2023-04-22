# DAGs and Tasks

In this topic we will learn the basics of building a data pipeline using a DAG. We begin by opening the Airflow Project on VSCode and creating a new file called `simple_dag.py` inside the DAGs directory.

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/dags_1.png?raw=true)

## DAG Skeleton

We also must begin by importing the DAG object from the airflow package. Next we can follow the basic template:

```python
from airflow import DAG

dag = DAG(...)
task_1 = Operator(dag=dag)
task_2 = Operator(dag=dag)
```

You can also use a with as statement to simplify the DAG declaration:

```python
from airflow import DAG

with DAG(...) as dag:
    task_1 = Operator()
    task_2 = Operator()
```

The most important DAG parameter to set is the DAG id. It must be a unique identifier otherwise features may start behaving strangely. We pass it as a parameter to the DAG object:

```python
from airflow import DAG

with DAG(dag_id = 'simple_dag') as dag:
    None
```

We can save this file and open the Apache Airflow user interface to verify the DAG is actually defined. Notice that the DAG, by default, contains no owner and is scheduled to run daily.

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/dags_2.png?raw=true)

## Demystifying DAG Scheduling

The next two important parameters we must define for the DAG are the start date (from where the scheduling date starts runnings) and the schedule interval (the interval between DAG runs). Understanding how tasks are scheduled is crucial for an airflow user.

We begin by exploring three parameters:

- start_date: The data to initiate the execution of the data pipeline. e.g '01/01/2021 00:00:00'.
- schedule_interval: Period of time between DAG runs. e.g '00:10:00'.
- end_date: Defines the date at which the DAG stops being scheduled. e.g '02/01/2021 00:00:00'.

The first DAG trigger will happen from the start date + the schedule interval. For this example, the first DAG run will happen on '01/01/2021 00:10:00'. This is the execution_date after the DAG run has finished (since the execution date refers to the last successful execution).

### Using the start_date

We can begin using the start_date parameter. An observation is the airflow dates should always be in UTC. 

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from datetime import datetime # For specifying the start date

with DAG(dag_id = 'simple_dag', start_date = datetime(2021,1,1) ) as dag:
    task_1 = DummyOperator(
        task_id = 'task_1'
    )
```

If we don't specify the start date, we get an error in the Airflow GUI. We could also specify the start date at the operator level:

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from datetime import datetime # For specifying the start date

with DAG(dag_id = 'simple_dag', start_date = datetime(2021,1,1) ) as dag:
    task_1 = DummyOperator(
        task_id = 'task_1',
        start_date = datetime(2021,1,2)
    )
```

But this shouldn't be done, since tasks will the start in different dates. 

Also, whenever a start_date is in the past, Airflow will run all the past, non-triggered runs (between the start date and now).

It's also good practice to not use dynamic dates. 

### Using the schedule_interval

By default, this is set to 24h. In the DAG object, we can pass a schedule_interval, which can be a CRON expression or a timedelta object. The schedule_interval can also be set to "None". This defines that the DAG can only be triggered manually or by an external trigger. 

### CRON Expression

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from datetime import datetime # For specifying the start date

with DAG(dag_id = 'simple_dag', schedule_interval = '*/10 * * * *', start_date = datetime(2021,1,1)) as dag:
    task_1 = DummyOperator(
        task_id = 'task_1'
    )
```

### Airflow Interval Tags

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from datetime import datetime # For specifying the start date

# Or @monthly or @weekly
with DAG(dag_id = 'simple_dag', schedule_interval = '@daily', start_date = datetime(2021,1,1)) as dag:
    task_1 = DummyOperator(
        task_id = 'task_1'
    )
```

### Using timedelta

One of the differences between the CRON object and timedelta is that with CRON we can set absolute date times to run the DAG. With timedelta, we cannot do this. 

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from datetime import datetime, timedelta

# Or @monthly or @weekly
with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date = datetime(2021,1,1)) as dag:
    task_1 = DummyOperator(
        task_id = 'task_1'
    )
```

### Backfilling and Catchup

The process of backfilling allows us to rerun past non-trigerred or already triggered DAG runs. For example, if a mistake is made, and a fix happens after 5 days, we will have non-trigerred DAG runs. This will be automatically triggered by airflow. Airflow will also trigger non-triggered DAG runs between the start date and the latest date.

To disable enable this process, the catchup parameter can be passed as True or false to the DAG definition.

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.utils.dates import daysago
from datetime import datetime, timedelta

# Or @monthly or @weekly
with DAG(
    dag_id = 'simple_dag', 
    schedule_interval = timedelta(hours=7), 
    start_date =days_ago(3)
    catchup=False
    ) as dag:

    task_1 = DummyOperator(
        task_id = 'task_1'
    )
```

To limit the number of DAG runs running in parallel you can use the max_active_runs in the DAG definition. 

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.utils.dates import daysago
from datetime import datetime, timedelta

# Or @monthly or @weekly
with DAG(
    dag_id = 'simple_dag', 
    schedule_interval = timedelta(hours=7), 
    start_date =days_ago(3)
    catchup=False,
    max_active_runs=3
    ) as dag:

    task_1 = DummyOperator(
        task_id = 'task_1'
    )
```

With catchup parameter set as false, the backfilling process can be executed in the command line.

## Operators

An operator is a task. This becomes automatically a task. Two tasks, such as extracting data and cleaning data, shouldn't be in two tasks. If a task fails, we must retry both tasks. Instead, by separating the task, we only retry the failed task. One operator should always be a task.

Also, the same input must always produce the same output for the task. This concept is very important.

The task ID must also be unique between all operators in the DAG. Also, many different parameters for the operator can be specified, such as retry for retrying after fails, with retry_delay with a timedelta a try can be scheduled in an interval of task.

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.utils.dates import daysago
from datetime import datetime, timedelta

# Or @monthly or @weekly
with DAG(
    dag_id = 'simple_dag', 
    schedule_interval = timedelta(hours=7), 
    start_date =days_ago(3)
    catchup=False,
    max_active_runs=3
    ) as dag:

    task_1 = DummyOperator(
        task_id = 'task_1',
        retry=5,
        retry_delay=timedelta(minutes=5)
    )
```

Also, the default parameters such as retry and retry_delay can be set globally for the DAG. This can be done using the default_args argument for the DAG:

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.utils.dates import daysago
from datetime import datetime, timedelta

default_args = {
        'retry':5,
        'retry_delay':timedelta(minutes=5)
}

# Or @monthly or @weekly
with DAG(
    dag_id = 'simple_dag', 
    schedule_interval = timedelta(hours=7), 
    start_date =days_ago(3)
    catchup=False,
    max_active_runs=3,
    default_args = default_args
    ) as dag:

    task_1 = DummyOperator(
        task_id = 'task_1',
    )
```

The baseoperator class specifies all the basic parameters that can be applied to all operators.

### Executing Python Functions

The most commonly used operator in Airflow, the PythonOperator can be used. The Python operator requires a Python function to be called with the python_callable argument.

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.operators.python import PythonOperator # Operator for executing Python funcs
from airflow.utils.dates import daysago

from datetime import datetime, timedelta

default_args = {
        'retry':5,
        'retry_delay':timedelta(minutes=5)
}

def _downloading_data():
    print('testing...')

# Or @monthly or @weekly
with DAG(
    dag_id = 'simple_dag', 
    schedule_interval = timedelta(hours=7), 
    start_date =days_ago(3)
    catchup=False,
    max_active_runs=3,
    default_args = default_args
    ) as dag:

    task_1 = PythonOperator(
        task_id = 'task_1',
        python_callable=downloading_data
    )
```

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.operators.python import PythonOperator # Operator for executing Python funcs
from airflow.utils.dates import days_ago
from datetime import timedelta

def do_nothing():
    return None

with DAG(dag_id = 'simple_dag',start_date =days_ago(1), schedule_interval = timedelta(hours=7)) as dag:

    task_1 = PythonOperator(
        task_id = 'task_1',
        python_callable=do_nothing
    )
    task_2 = DummyOperator(
        task_id = 'task_2'
    )

    task_1
    task_2
```

A very important aspect of the PythonOperator is accessing the context of the DAG run, such as the current execution date. The **kwargs parameter can be added to the Python function and printed. This passes the context into the Python function. This can for example access the DAG/DAG run objects. 

To access the DS field from the context dictionary for example

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.utils.dates import daysago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
        'retry':5,
        'retry_delay':timedelta(minutes=5)
}

def _downloading_data(ds):
    print(ds)

# Or @monthly or @weekly
with DAG(
    dag_id = 'simple_dag', 
    schedule_interval = timedelta(hours=7), 
    start_date =days_ago(3)
    catchup=False,
    max_active_runs=3,
    default_args = default_args
    ) as dag:

    task_1 = PythonOperator(
        task_id = 'task_1',
        python_callable=downloading_data
    )
```

We can also specify the argument such as op_kwargs to specify a dictionary and pass parameters to the function. This must be defined in the Python function arguments.

```python
from airflow import DAG
from airflow.operators.dummy import DummyOperator # Operator that does nothing
from airflow.utils.dates import daysago
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
        'retry':5,
        'retry_delay':timedelta(minutes=5)
}

def _downloading_data(my_params, ds):
    print(my_params, ds)

# Or @monthly or @weekly
with DAG(
    dag_id = 'simple_dag', 
    schedule_interval = timedelta(hours=7), 
    start_date =days_ago(3)
    catchup=False,
    max_active_runs=3,
    default_args = default_args
    ) as dag:

    task_1 = PythonOperator(
        task_id = 'task_1',
        python_callable=downloading_data,
        op_kwargs={'my_params':42}
    )
```

### Putting the DAG on Hold

**Sensors:** A sensor is a special kind of operator that waits for something to happen before moving to the next file. 

Sensors can be useful to wait for an event. For example, we can use the FileSensor to wait for a file to be created in a directory.

```python
from airflow import DAG
from airflow.utils.dates import daysago
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

default_args = {
        'retry':5,
        'retry_delay':timedelta(minutes=5)
}

def _downloading_data(**kwargs):
    with open('/tmp/my_file.txt', 'w') as f:
        f.write('my_date')

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    downloading_date = PythonOperator(
        task_id = 'downloading_date ',
        python_callable=downloading_data,
        op_kwargs={'my_params':42}
    )

    waiting_for_data = FileSensor(
        task_id = 'waiting_for_data',
        fs_conn_id='fs_default',
        filepath='my_file.txt',
        poke_interval = 15 
    )
```

The FileSensor must receive a fs_conn_id argument which is a file connection ID. The default argument can be used to specify a Airflow Connection previously configured on the UI. The filepath must also be specified. The poke interval is the amount of time it takes the sensor to perform checks for the event.

By going to "Admin > Connections" the connection can be created. By clicking on the plus sign and "add a new record" the file connection can be configured. The ID field specifies the identifier of the connection + configuration. The connection type specifies the type of service to be connected to. For the file connector the extra JSON can be the path for the file:

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/dags_3.png?raw=true)

### Executing Bash commands

Another common operator is the bash operator, which allows executing bash commands. The bash operator receives a basic parameter that specifies the bash command to be executed.

```python

from airflow.operators.bash import BashOperator

...

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    ...

    processing_data = BashOperator(
        task_id="processing_data",
        bash_command="exit 0"
    )
```

### Defining Task Paths

One very important step is to speficy the execution order for tasks. This allows us to specify dependencies between tasks. There are two ways to do this.

First, the set_downstream/set_upstream can be used. For downstream, the object that calls the method is executed first, and the parameter after. For upstream, the parameter is executed first, and the object that calls the method later.

```python

from airflow.operators.bash import BashOperator

...

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    ...
    # The first task to execute is the object
    downloading_data.set_downstream(waiting_for_data)
    waiting_for_data.set_downstream(processing_data)
```

```python

from airflow.operators.bash import BashOperator

...

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    ...
    # The first task to execute is the parameter
    waiting_for_data.set_upstream(downloading_data) 
    processing_data.set_upstream(waiting_for_data) 
```

There is a better way to do this with the left and right bitshift operators:

```python

from airflow.operators.bash import BashOperator

...

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    ...
    downloading_data >> waiting_for_data >> processing_data # set downstream
    processing_data << waiting_for_data << downloading_data # set upstream
```

If we want to execute multiple tasks in parallel, they can be put in parallel:

```python

from airflow.operators.bash import BashOperator

...

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    ...
    downloading_data >> [waiting_for_data, processing_data]
```

Airflow also brings helpers to structure this path. The chain function can be used to pass the sequence as a sequence of arguments instead of a sequence of bitshits:

```python

from airflow.models.baseoperator import chain

...

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    ...
    # Same as downloading_data >> waiting_for_data >> processing_data
    chain(downloading_data, waiting_for_data, processing_data)
```

The second function that can help is the cross downstream function:

```python

from airflow.models.baseoperator import cross_downstream

...

with DAG(dag_id = 'simple_dag', schedule_interval = timedelta(hours=7), start_date =days_ago(3), catchup=False,max_active_runs=3,default_args = default_args) as dag:

    ...

    cross_downstream([downloading_data, checking_data],[waiting_for_data, processing_data])
```

This generates the following DAG. Processing data depends on downloading_data and checking_data, and waiting_for_data depends on both as well. This should be used when two lists of tasks require dependency. If the bitshift operator is used, the DAG fails.

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/dags_4.png?raw=true)

### Exchaging Data

Data can be shared between tasks but there are some limitations. This is done with XCOMs. 

**XCOM:** Cross communication. Allows us to exchange small amounts of data between tasks.

A XCOM is created when a value is returned from a function for example. Another way is to use xcom_push.

```python
def _downloading_data(ti):
    my_xcom = ti.xcom_push(key='my_key', value='42')
    return '42' # both work
```

Then we can pull the XCOM using xcom_pull.

```python
def _checking_data(ti):
    my_xcom = ti.xcom_pull(key='return_value', task_id =['downloading_data'])
    my_xcom2 = ti.xcom_pull(key='my_key', task_id =['downloading_data'])
    print(my_xcom)
```

XCom are stored in the metadatabase of airflow. With this, there are limitations of size of what can be written with XCom. It's not recommended to process gigabytes of data. 

### Handling Failures

When tasks fail (an error happens during the code execution), Airflow tries to retry them.  Retries for the tasks can be set using the arguments 

- 'retries' which specifies the maximum number of retries
- 'retry_delay' which specifies the wait interval between retries
- 'email_on_failure' boolean that tells the administrator a failure happened.
- 'email_on_retry' boolean that tells the administrator that a task is up for retry.
- 'email' email to send the information emails to.
- 'on_failure_callback' can be given a function to trigger when the task fails.

The task can be retried by clicking on clear. It allows us to retry and overwrite the failed task execution.

If we have multiple task fails, we can add a filter by state in the Admin > Task Instance window and add the filter "up_for_retry". We can also filter by the DAG ID. All the tasks can be selected and be cleared at once. This allows us to retry all tasks at once. 

# Resources
