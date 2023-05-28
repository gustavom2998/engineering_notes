# 3 - Ingesting Data

## Choosing Tools

- We require a minimum level of organization in the data lake.
- Chose a categorization method based on the access pattern of processing methods.
- Auto-generated data
  - Data from IOT devices, server logs, etc.
  - Streaming and unstructured.
  - Suggested architecture:
    - Ingestion with Amazon Kinesis.
    - Store on S3.
    - Catalogue with glue.
    - Process with Lambda.
    - Query with Athena.
- Operational Data
  - From inventory, sales, expense reports, etc.
  - Batched data.
  - Consumed for Analytics.
  - Suggested architecture:
    - Ingestion with API Gateway.
    - Storage with S3.
    - Catalogue with Glue.
    - Transport to Elasticsearch.
    - Analyse with Kibana.
- Manually generated data
  - Social media feeds, contact forms, call center, audio, emails.
  - Suggested architecture:
    - Ingest with files AWS Transfer or Appflow.
    - Store on S3.
    - Catalogue with Glue.
    - Amazon Comprehend to process and analyse data.

## Data Structures

- Structured data
  - Easy for a computer system to consume without modification.
  - Normally available in relational databases.
- Unstructured data
  - Type of content (not actual file format)
  - Can be large chunks of unstructured text data.
  - Normally use EMR and Glue to process this data.
  - Data can be loaded into structured services that improve performance at a lower cost.

## Processing

- Data can be processed at different stages of the data lake.
- ETL
  - Extract, transform and load.
  - This concept has been around for some time.
  - Applicable when we must remove/format part of the data before storing it.
- ELT
  - Swapped order.
  - Preserving raw data avoids losing any information.
  - After data is stored, it can be processed.
- ETLT
  - Two transformation steps.
  - Transform data right after extraction.
  - Load it onto a platform.
  - Posteriorly perform processing of complex data.
  - Process any data that was added during ETL.
  - The first is normally a minor processing task, the second is a major task.

## Data Streaming Ingestion with Kinesis

- Streaming consists of a high volume of small packets of data.
- High volume with low latency = Elevated costs.
- Batch processing can be optimized to be cheaper if a longer time to insight can be afforded.
- Amazon Kinesis Family
  - Streaming services.
  - Data Stream, Analytics, Firehose and Video streams.

### Kinesis Data Streams

- Receives data from producers.
  - IOT Sensors, Web server logs, clickstream data, etc.
- Feeds into consumers.
  - EC2, Lambda Functions
- Data Agnostic
  - The same stream can process different types of data.
  - Data can be separated by type or have a single stream.
- Data retention and consumption replay.
  - Retention: Data stays in the stream (even if it has been consumed).
  - 24h retention by default.
  - Can be extended (but increases costs)
  - Data can be consumed by multiple users at the same time.
- Pull based
  - A consumer connects with Kinesis using Library.
  - The consumer is written for getting data, processing and storing it somewhere.
  - Real-time analysis of data that passes through the stream.

### Kinesis Firehose

- Created based on user behaviour.
- Can easily be configured to store on S3, Redshift, Elasticsearch, HTTP Endpoint.
- Automatically scales to match throughput.
- Can batch, compress, transform and encrypt data before loading.
- Lambda functions can be used to process Firehose data as a push-based architecture.
  - Easier than hosting consumers on EC2

### Kinesis Analytics

- Serverless analytics on data stream without having to write code.
- Supports SQL queries and Apache Flink.
- Data can be mapped into an application stream that can be queried like a table.
- Data can be pumped into the application stream.

### Kinesis Video Streams

- Ingest video data from connected devices.
- Integrates with IOT devices such as doorbell cameras.
- Can be used to ingest the data and make it available for processing.

## Batch Data Ingestion

- Data has been produced and is unavailable at a remote location.
- Internet upload might be unreliable due to a large volume of data.

### AWS Transfer Family
- Serverless service.
- Provides file transfer endpoint for ingesting data.
- Logs all activity on Cloudwatch.

### AWS Snow

Services for offline data transfer.

#### AWS Snowcone

- Tamper proof, dust proof, water resistance device.
- Powered by USB-C.
- Terabytes of usable storage.
- Reduces time to upload/risk of failure with limited broadband.
- Shipped by Amazon.
- File transfer over 10GB Ethernet.
- GUI for uploading, encrypting and securing data.
- Contains a display with return information if lost in shipping.

#### AWS Snowball

- More capacity than AWS Snowcone.
- Bigger, heavier and denser.
- 50TB storage per device.
- Snowballs can be clustered.

#### AWS Snowmobile

- Petabytes of storage.
- Data Center on wheels.
- Exabyte scale data transfer service.
- Can be used for migrating data into AWS.
- Can transfer up to 100PB to AWS.
- Not very commonly used.

## Data Cataloguing

- Need to keep track of all assets on the data lake.
- Also needs to track the virtues of transformed data.
- Multiple services can be used for cataloguing S3 data.
- The catalogue should provide a single source of truth about the data.
- There are two general forms of cataloguing:
  - Comprehensive Data Catalog
    - Used to search for assets.
    - Data sources are stored on S3.
    - Lambda is used to extract metadata from data that arrives.
    - Lambda trigger store metadata on DynamoDB.
    - Lambda indexes information on Elasticsearch.
    - The user can search the databases to find objects that meet search criteria.
  - Hive Data Catalogue
    - Contains information about assets.
    - Data is ready to be used by processing services.
    - Common to be made of Glue tables and databases.
      - Store: Physical location of data on S3.
      - Table: External reference to data stored on S3.
    - Tables can be processed with Athena or Hadoop.
    - Converting files to tables:
      - The catalog indicates Serializes/Deserializers to parse data.
      - The catalogue defines row format, stored as input format and output format.
      - The catalogue has a table schema with columns and datatypes (like SQL).
      - The table schema can be inferred automatically by Glue Crawler.
- Most data lakes contain both types of catalogues.
- They complement each other.
- With the comprehensive catalogue, assets can be found and analyzed.
- With Hive Catalogue, transformations and analysis can be performed.  
