# Using Apache Airflow

There are three different ways of interacting with Apache Airflow.

**USER INTERFACE:** Used extensively since it allows us to manage and monitor data pipelines. If we want to check logs, get history of DAG runs, we will probably use the UI.

**COMMAND LINE INTERFACE:** Useful in some special cases such as testing tasks, upgrading or initializing airflow. Or for some reason the user interface is not accessible.

**REST API:** Useful for building a platform on top of airflow, such as front-end that triggers a DAG. 

In this module we will explore what the different methods are and their use cases.

## User Interface

Below, we list the many user interface components and how to interact with them via the user interface.

### DAGs View

The default view for Apache Airflow is the DAGs view. It will be used a lot since it allows us to list all DAGs and other information.

### The DAGs Table

**Toggle:** In the DAG table we have a toggle next to the DAG name. This defines whether or not a DAG is ready to be scheduled or not. If we want to start scheduling tasks, we need to turn on this toggle. If you want to pause a DAG (because it contains a mistake for example), the toggle can be used to turn it off.

**Name:** The name of the DAG.

**Owner:** The owner of the DAG task. Useful with cluster policies that prevents certain users to run specific DAGs. 

**Runs:** The status of the current or historical DAG runs. From left to right the circles list the: Number of succeeds; number of running; number of failed.

**Schedule:** The schedule interval defines the interval of time in which the DAG is triggered.

**Last Run:** The execution date of the last DAG trigger. It's not the last time the DAG was triggered, but it corresponds to the beginning of the scheduled interval (latest execution data).

**Recent Tasks:** Doesnt show the status of all the tasks that have been executed in the past, only the current running or the latest ones. 

**Actions:** 

- **Manual trigger:** play button - toggle needs to be turned on.
- **Refresh DAG:** to force update the DAG with some modifications from the code without having to wait default parse time.
- **Delete DAG:**  This deletes the metadata related to the DAG. The file must be manually removed.

**Links:** Other complimentary views such as Code, details, Gantt Chart, Landing, Tries, Duration, Graph view, Tree view. 

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/using_airflow_1.png?raw=true)

After turning on the Example DAG:

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/using_airflow_2.png?raw=true)

### Tree View

When we click on a DAG we see the tree view. It allows us to get the history along with the current runs and the status of the tasks. The square colours indicate the status of the task. the Circles correspond to DAG runs and the square the TASK. It's useful to spot if a DAG is running late or if there was an error. 

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/using_airflow_3.png?raw=true)

### Graph View

It's great to check the dependencies of the data pipeline and for observing the latest DAG run. The rectangle corresponds to the task and the border colour to the status of the task. It's great to grasp the structure of a single run of the data pipeline. You can view the history of the DAG runs by selecting the DAG run in the toolbar above the graph. 

 

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/using_airflow_4.png?raw=true)

### Gantt View

Allows us to analyse task duration and overlaps. It's great for finding bottlenecks. The larger the rectangle, the longer it takes to execute a task. By looking at overlaps, we can see that tasks were executed in parallel. 

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/using_airflow_5.png?raw=true)

### Interacting with Tasks

One question may be interacting with tasks. We may want the logs of a given task. If we click on a task, we land on the task instance context menu. 

![Untitled](![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/using_airflow_6.png?raw=true))

**Instance details:** We can get instance details, which lists the properties of the object. 

**Rendered:** Allows us to see the output of the task data. 

**Log:** If we click on it, we can see the output and if the task was a success or not.

**All instances:** Check all task instances for a given task across all DAG runs. Create to check the history a task

**Filter Upstream:** Filters the view to see only dependent tasks. 

Besides that we also have task actions:

- Run: We can run the task (with the right executor)
- Clear: If a task fails, you can clear it to restart the task.
- Mark Failed and Mark Sucess: Useful for testing how the pipeline behaves on failure/success.

## Command Line - Useful Commands

In this section, we list some useful commands that can be executed from the command line.

Extremely useful to use for executing commands that are not available on the UI. Also, sometimes the UI might not be available.

To connect to the docker container for a resource we can execute the following commands:

```bash
docker ps // List active docker containers to the the ID of the web server
docker exec -it {web-server-id} /bin/bash // Access the resource given the id using Bash

airflow db init       // Initialize the database
airflow db upgrade    // Update Airflow metabase with new version
airflow db reset      // Allows us to remove everything from the database
airflow webserver     // Start the web server for the UI
airflow scheduler     // Start the scheduler
airflow celery worker // Start a celery worker - indicate that this execution is available for executing tasks - useful for executing tasks on clusters
airflow dags pause    // Toggle - disables/enable scheduling for a DAG - can also use the argument unpause
airflow dags trigger  // Manually trigger a DAG or specify an execution date with -e argument
airflow dags list     //  Lists dag id, filepath, owner and if it is paused or not
airflow tasks list {dag-id} // List all tasks the DAG contains
airflow tasks test {dag-id} {task-id} {execution_date} // Execute a task without checking a dependency - use this command to test a task works
airflow dags backfill -s {startdate} -e {enddate} --reset {dagid} // Re-run past DAG runs - arguments: start date; end date; reset_dagruns
```

## REST 

The last method of interacting with Airflow is with the REST API.

Currently contains a stable build with Airflow 2.0. Most endpoints contain CRUD operations. It can be connections, DAGs, DAG runs, etc. 

New tools can be built on top of airflow and integration can be built with new tools.

See the documentation for more information:

[Airflow REST API](https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html)

# Resources