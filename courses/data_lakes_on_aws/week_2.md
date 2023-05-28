# 2 - Exploring Data Services

## Service Categories

Decoupled layers - managing, scaling and securing becomes easier

- Data Storage and Cataloguing
  - Focus on building the data lake.
- Data Movement
  - Once we know how to build, we can ingest the data.
  - We can move data from the source into the data lake.
- Analytics and Processing
  - When and what services to use to process and analyze data
  - Run SQL Queries, Join data, and feed into dashboard, generate business report

## Storage and Cataloguing

### Requirements

- Support petabytes of data
- Scalability
- Able to store structured and unstructured data
  - Discards databases

### Object Storage

- S3 and S3 glacier are great for this
- Schema on read model works because data is stored as objects
- Everything in centralized for the organization
- Not limit to bucket size
- Scaling is handled by the service
- Very durable
- Integrates very well with other services
- There are configurations for reducing costs
  - Different storage tiers that are cheaper
  - Infrequently accessed data can be moved to tiers that charge less for volume but more for access.
  - Frequently accessed data can be moved to tiers that charge more for volume but less for access.
  - There are tools to monitor and manage object tiering.

> Alternatives: Google Cloud Storage, Azure Blob Storage, Self hosted Minio on K8s.

### Metadata Catalog

- Raw assets can be of many types, hard for user to analyze and find
- Data can change over time, versioning is important
- Data Swamp
  - Lots of data
  - Not used because its unknown
  - Can be fixed with metadata and cataloguing
- AWS Glue
  - Fully managed serverless data processing and cataloguing service
  - Amazon calls it an ETL service
- Glue crawler populates catalog with tables
  - Triggered to analyze data in S3 and infer a schema format and data type.
  - Classifiers can analyze JSON, but there are others. 
  - Eliminates need to define schemas manually.
  - Ca nbe configured to update, delete, or compare schema changes
- Glue Data Catalog is central metadata repository
  - Contains tables which are metadata definitions that represent data
  - Table has a schema and organized into databases
  - Data acn be used to help author ETL jobs
- ETL Engine can be used to automatically generate Python/Scala to process data with Spark
- Scheduler can handle dependency resolution, job monitoring and retries.

> Alternatives: Kind of hard to say. Glue bundles many services into one and is very expensive. Google Cloud Dataplex covers search/cataloguing. Azure also has its own Data Catalog Service. Azure Data Factory can be used for ETL. Overall I've had little contact with these services, and mostly find them interesting for finding data, but have never been in a situation where I've used them to their full potential. Also, a cool open alternative I once checked out was [Datahub](https://datahubproject.io/).

## Data Movement

### Streaming Data

- Kinesis Data Streams and Firehose can be used to ingest real time data.
- Kinesis Data streams
  - Collect data from various sources
  - Continuously process data
  - Can generate metrics, power dashboards or aggregate and store data.
  - AWS SDK must be used to process data
  - Incoming data is organized into shards
  - Shards can be scaled in/out
  - Data stored in shards can be processed by one or multiple consumers using the SDK
- Kinesis Firehose
  - Also real time ingestion
  - No need for SDK
  - Configure where o write data
  - Data sent to it will be written to the output
  - Simpler alternative

> Alternatives: Google Pub/sub, Apache Kafka. I've experimented with the other two as well and it's mostly the same concepts with different SDKs. Apache Kafka has the problem with managing it if it's self hosted.

### RESTful ingestion

HTTP is a simpler and more cost effective solution to streaming.

- API Gateway is a service that allows hosting API that acts as a interface to a backend.
- The backend could be an app on EC2, Lambda Function or Another service like Kinesis.
- Data can be sent to the API with HTTP, which is simpler for publishing data.
- This doesn't have as many features.

### SaaS Integrations

Another way to integrate data is with SaaS integrations.

- AWS Appflow offers integrations with common data sources and AWS sources
- It can be used to ingest data from SaaS services into the data lake
- Common services include Salesforce, Slack, Google Analytics, etc.
- There is no need to write custom connectors.
- Data is written to S3, and can quickly be analyzed with a processing solution.

> Alternatives: Google Cloud Data Fusion, Stitch, Airbyte, Fivetran.

## Data Processing and Analytics

### Data processing

- Need to adjust data before analysis
- Data needs to be correctly formatted and cleaned (missing fields, deduplication)
- This can be done via batch jobs or via streaming
- Batch data transformation
  - Scripts to fix errors, reformat data, etc.
  - Apache Hadoop
    - Open source framework for distributed data processing
    - Great for large amounts of data
    - Hadoop runs on clusters of multiple computers to analyze massive datasets in parallel quickly.
  - Amazon EMR
    - Managed cluster platform that allows distributed data processing
    - Compute and storage is decoupled
    - Great for batch data processing
    - Long running or transient clusters can be configured
  - Amazon Glue
    - As mentioned before, Glue can be used for ETL Jobs
    - Jobs have configurations instead of clusters
    - Jobs can have data sources, targets, transformation scripts and other settings
    - Can run on a schedule or be triggered by an even
    - Glue orchestrates infrastructure.
    - Basically serverless hadoop.

> Alternatives: Google Dataproc, Azure Databricks.

- Real time data transformation
  - AWS Lambda
    - Serverless compute service that runs on demand
    - Can be triggered by Kinesis
    - can be used to pre-process data before sending it down stream

> Alternatives: Google Cloud Functions, Azure Functions, Cloud Run.

### Analytics

