# Introduction

Course reference link: https://academy.astronomer.io/astronomer-certification-apache-airflow-fundamentals-preparation

# Notes

Topics to be discussed:

- Introduction
    - Use cases for Apache Airflow, when it's suitable to be used and not used
    - Different components such as Web server, Scheduler, Metabase
    - Core concepts such as DAGs, task instances, and operators.
    - How to update Airflow
- Using Airflow
    - Command Line Interface
    - User interface
    - Rest API
- DAGs
    - Basics: Minimum Requirements and Parameters
    - Monitoring DAGs using UI
    - Sharing data between DAGs with XComs
    - Connections with separate operators
- Parallelism
    - Executors (multiple tasks in parallel)
    - Parallelism Parameters, Concurrency, etc.

# Running Airflow 2.0 with Astro CLI

Begin by downloading and installing Docker using Convenience Script ([see link](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script)):

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

Next install docker compose:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Install the Astronomer CLI

```bash
curl -sSL https://install.astronomer.io | sudo bash
```

Confirm they're all correctly installed

```bash
docker --version
docker-compose --version
astro version
```

Initiate a Docker process in a separate terminal. Leave running

```bash
sudo dockerd
```

Create a new astro project

```bash
mkdir astro
cd astro
astro dev init
sudo astro dev start

```

List the running containers for Airflow. Contains three different resources: The database (POSTGRES), the Scheduler and the Webserver

```bash
sudo astro dev ps
```

![Untitled](courses/airflow_fundamentals/images/introduction_1.png)

![Untitled](https://github.com/gustavom2998/engineering_notes/blob/main/courses/airflow_fundamentals/images/introduction_1.png?raw=true)

The web server can be accessed from the browser by going to the URL [localhost:8080](http://localhost:8080).

Authenticate with admin:admin.

![Untitled](courses/airflow_fundamentals/images/introduction_2.png)

We're on the Airflow web console, where we can interact with Airflow

![Untitled](courses/airflow_fundamentals/images/introduction_3.png)

 

# Resources