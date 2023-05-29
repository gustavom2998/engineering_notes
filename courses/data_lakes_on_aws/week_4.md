# 4 - Processing Data

## Data Prep

- Making data useful is hard and takes up time.
- Data needs to be prepared to be used by services.
- The same data may be reprocessed for different use cases.
- Processing needs to be future-proof.
- Raw data must be preserved - treat it as immutable.
  - This can be configured on the object storage service.
- Data can be copied and processed
  - Shaping: Select, combine, transform or aggregate data (in regards to the schema).
  - Blending: Taking datasets from different schemas/formats and matching them in a format that can be analyzed.
  - Cleaning: Fill in missing values, solve data conflicts and normalize the data to meet common definitions.
- Automation is key when performing these steps.
- Tools can be used to automate these tasks.

## Glue Jobs

- Triggered based on triggers or schedule.
- Best for processing data in batches.
- A job is the business logic that performs the ETL work on AWS Glue.
- A job can be defined by following these steps:
  - Define the sources for the job (they must exist in the data catalogue).
  - Provide configurations for the job such as the framework to use (Spark on Scala, PySpark).
  - Provide transformation configuration.
  - Logging and monitoring requirements.
  - Glue generates a PySpark script.
  - The script can be edited to add transforms, additional code, etc.
  - We can schedule or define a trigger for the job.
- Glue jobs are great for users who aren't used to setting up/working with Spark.

## Lambda

- Triggered when data is uploaded to the data lake.
- Best for processing real-time data.

## File Optimizations

- CSV files use row-oriented storage
  - If we want to query the average of a column.
  - The entire block is loaded.
  - Only a part of the block is read.
  - Great for adding new records and sorting.
- Column-oriented formats use columns for blocks
  - Only the required columns are loaded.
  - Great for analytics and compression.
  - E.g: Parquet and ORC.
  - Great for Athena
    - Compress by column.
    - Athena can fetch only the blocks it needs.
    - Based on the predicates for a query, Athena can determine whether to read or skip a block.
    - Athena can split reading data to multiple readers to increase parallelism during query processing.
- Compression is important for services that store/process data.
  - Based on data types.
  - Reduces costs and is faster.
  - No longer schema on read, but has good applications if raw data is preserved.
- Partitioning helps reduce data scan even more
  - Athena analyses the query and discards reading files from partitions that aren't present in the query.
  - This greatly decreases the amount of data scanned.

## Security

- Need to scope data access in a granular way.
- Producers of data need separate permissions to consumers.
- Need to analyse access patterns to then define security rules.
- Each entity should have the minimum necessary permissions to do its tasks.
- Sensitive data needs to follow compliance programs.
- Audits are good practice for security.
- Enabling logging and monitoring for API calls is also good security practice.
- Services like Athena can be used to query and analyze logs.

### Securing S3

- Enable S3 encryption at rest.
- Configure S3 bucket access policies.
- Block public access.

### Securing Glue

- Enable encryption at rest for Data Catalogue.
- Use IAM Policies to allow/deny actions for specific users.
- Add resource-based policies to apply different policies to different resources.

## Data visualization

- Involves taking abstract data and representing it in an interactive visual to produce insights.
- Example clickstream
  - Generate clickstream data.
  - Store on S3.
  - Analyse user interaction.
  - Build a click map.
  - Determine where to place advertisements or new features.
- Example Restaurant
  - Take Sales, Visitors, Reservation and Financial data.
  - Visualize the data to compare branches.
  - Graph data to view sales by day.
  - Visualize the comparison of branch sales.
  - Cross with external data (traffic, weather, economic).
  - Find new trends
    - Increased foot traffic has higher sales.
    - Sunny weather correlates with higher sales.
    - Decide where to open the next branch.

### Amazon Quicksight

- Data visualization service on Amazon.
- Connect to data we want to analyse.
- Use Quicksight to fine-tune data for visualization
  - Add calculated fields.
  - Apply filters.
  - Change field name/types.
  - Join tables from SQL sources.
  - Save preparation as part of the dataset.
- Create data analysis
  - Visual representations of the data.
  - Organize visuals into dashboards.
  - Share dashboards.
- AutoGraph: Quicksight feature which auto-selects visualization based on data.
- Positive points:
  - Native integration to Data Lake services.
  - Automatically scales infrastructure.
  - Adhoc transformations and analysis.
  - Super fast, parallel in-memory calculation engine (SPICE).
