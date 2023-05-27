# 1 - Introduction to Data Lakes

Whitepaper on [building data lakes](https://docs.aws.amazon.com/whitepapers/latest/building-data-lakes/building-data-lake-aws.html).

## Why data lakes

### Context

- Database causing bottlenecks
- Database being used for multiple use cases
  - Stream Data; Analytics; Syslogs; Customer Data
  - Called a one size fits all approach
  - Load issues
- Multiple databases can also be a problem
  - Difficult to catalog data
  - Security is hard to manage
- Tightly coupled storage and processing 
  -  harder to scale

### Proposal

- Break down and separate data components
- Enter data lakes
- Divide and conquer to separate different components
  - Storage
  - Ingestion
  - Analytics
  - Real time analytics
  - Machine Learning
- Solves the following problems
  - Increase operational efficiency
  - Increase data availability
  - Lower transaction costs
  - Offload capacity from databases and data warehouses

### Data Lake 

- Centralized repository to store structure and unstructured data
  - Lake name comes from supporting unstructured data
  - Data can be stored as is without structure
  - Analytics, processing and machine learning can be done on unstructured data
- No scaling restrictions
- Commonly deployed for analytics on
  - Transactions
  - Weblogs
  - Social Media
  - IOT

## Characteristics

- Data Agnostic: Any file type or structure.
- Variable applications: Catalogued data can be used for many different needs.
- Future proof: If the data is available, future questions can be answered.

## Components

Four main components:

- Ingest and store
  - Should be able to handle streaming and batch ingestion.
- Catalogue and search
  - Needs to have indexing and searching mechanisms to quickly find data.
  - Databases (SQL/NoSQL) can help with this.
  - Data lakes that aren't catalogued/hard to search are called data swamps.
- Process and serve
  - Can be done with Hadoop.
  - Combined with S3 storage - decouples storage.
  - Separate storage and compute.
- Protect and secure
  - Correctly configured permissions.
  - Shouldn't prevent unauthorized access.

## Data lakes vs Data Warehouses

### Data Warehouse

- System for reporting and data analysis
- Core for BI
- Central repository of integrated data from one or more sources

### Differences

1. Schema on Write vs Schema on Read
2. SQL vs Programming
3. Structured vs Unstructured Data

- They aren't the same thing
- Should be used together
- Ingestion into data lake then store cleaned data into Warehouse
- Data warehouses may be faster because of structured data
- One isn't better than the other for all use cases

## Sample Architectures

### Insights from Web Servers

- Number of Web servers
- Amazon Kinesis Agent can be used to send data
- Kinesis Firehose (ingestion service) receives data
- Data is stored on Amazon S3
- Amazon Athena can be used to process and analyze data stored on S3

> You pay for data in multiple points in this setup. You pay the fee for moving data with Kinesis, you pay for creating the S3 objects. You also pay for reading the S3 objects, and you pay for analysing those objects with Athena. This can be quite expensive if you don't carefully manage object sizes and counts well (Happened to me).
  
### Generic Data lake

- Data comes from other teams (not a specific use case).
- Kinesis firehose to S3.
- Lambda function triggered by S3 object creation.
- Lambda function code transforms data.
- Different tables store different types of objects.
- Lambda can also normalize data to fit into tables.
- Lambdas are good for renaming,parsing and normalizing data.

> Seems like a workaround for not working with Spark. Can be good for very simple pipelines, but doesn't seem very good for heavy processing jobs.

### Extending the Data Lake

- More tools can be added as the lake grows
- Ingestion layer can be extended with API Gateway to receive data via APIs
- Elasticsearch (full text search database) can be used for text search
- Kibana can connect to Elasticsearch for visualization


