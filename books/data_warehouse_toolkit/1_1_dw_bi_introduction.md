
# Data Warehousing and Bussiness Intelligence Introduction

## Data Capture vs Data Analysis

Information is normally used for two purposes:

1. **Operational systems:** for record keeping (data in).
    - Example: Taking orders.
    - Optimized to process transactions quickly, one transaction record at a time.
    - The tasks are predictable, repeated over and over for basic business processes.
    - Generally doesn't maintain history. Data is instead updated to reflect the latest state.
2. **Business Intelligence:** for Analytical Decision making (data out).
    - Example: Count new orders and compare them with last weeks orders.
    - Analyze data to evaluate performance and if processes are working correctly.
    - Need detailed data to support constantly changing questions.
    - Optimization for high-performance queries to analyze/transform of lots of transactions.
    - Historical data is preserved to be able to compare current data with past data.

- It's common to have DW/BI systems that are copies of the operational system stored on a separate hardware platform to improve performance. 
- Solves performance problems but ignores other problems. 
- Lazy solutions and don't acknowledge the different needs BI users have.

## DW/BI Goals

Before understanding how to build data warehouses, we must understand why users need them. The main reasons for needing a data warehouse are:

- Lots of data that needs to be accessed.
- Need to slice and dice the data.
- Business needs easy access to the data.
- Need to see what is important.
- Lack of agreement between numbers.
- Need to produce more information to base decisions on facts.

## DW/BI System Requirements

The basic requirements for a DW/BI system are:

- **Information availability**: Data Contents and BI Applications must be simple and fast for the business user to consume. Data must match business processes and vocabulary.
- **Information consistency**: Only release data when it's ready (quality-wise) to maintain credibility. Maintain label consistency. Same name = same definition. Different definition = Different name.
- **Adaptability to change**: Must be able to handle changes in technology, data, and business conditions without invalidating existing data. New questions/data should not disrupt existing data/applications. When data changes, the changes need to be handled to not impact downstream processes.
- **Timely performance**: Raw data needs to be converted into actionable information within the shortest possible time. The expectations for data prep and delivery times must be transparent for both DW/BI team and users.
- **Security and privacy**: Access control to protect organizations confidential information.
- **Drive decision making**: Needs to have the right data to support this process. Main Outputs: the decisions that are made based on the data.
- **Usage and adoption**:  No matter how well-built the system is, it needs to be used to produce impact. Acceptance is also a test. Business users embrace simple and fast systems.

## DW/BI System Architecture

To maintain a DW/BI system over time, here is an overview of tips and responsibilities:

- **Understand your users**: Job, responsibilities, goals and objectives. Find out the decisions they want to make based on data. Find the best users for making high-impact decisions. Find new users and present them to the system.
- **Make sure the data being delivered is correct, relevant and accessible**: Present the most robust and actionable data. User interfaces should be simple. Validate and monitor data accuracy and quality. Adapt the system to changes in business priorities and data availability.
- **Maintain the system**: Justify investments by presenting decisions made using the system. Deliver regular updates. Maintain business users trust. Keep users, executives and tech teams happy.

## Reference

Personal notes for educational purposes based on the book [The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) by Ralph Kimball and Margy Ross, 3rd edition.
