# Data Warehouse, Bussiness Intelligence and Dimensional Modelling

## Summary

- Overview of Data warehousing and Bussiness Intelligence systems
- Analyze business needs for a data warehouse
- Work backwards to the logical and then physical designs, as long as with decisions about technologies and tools.
- Introduce dimensional modelling concepts and vocabulary
- Kimball DW/BI architecture along with alternatives
- Review common myths and misconceptions about DW/BI

## Data Capture vs Data Analysis

Information is normally used for two purposes:

1. **Operational systems:** for record keeping (data in).
    - Example: Taking orders.
    - Optimized to process transactions quickly, one transaction record at a time.
    - The tasks are predictable, repeated over and over for basic business processes.
    - Generally doesn't maintain history. Data is instead updated to reflect the latest state.
2. **Business Intelligence:** for Analytical Decision making (data out).
    - Example: Count new orders and compare them with last weeks orders.
    - Analyse data to evaluate performance and if processes are working correctly.
    - Need detailed data to support constantly changing questions.
    - Optimization for high-performance queries to analyse/transform of lots of transactions.
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

The basic requirements for a DW/BI system are:

- **Information availability**: Data Contents and BI Applications must be simple and fast for the business user to consume. Data must match business processes and vocabulary.
- **Information consistency**: Only release data when it's ready (quality-wise) to maintain credibility. Maintain label consistency. Same name = same definition. Different definition = Diferent name.
- **Adaptability to change**: Must be able to handle changes in technology, data, and business conditions without invalidating existing data. New questions/data should not disrupt existing data/applications. When data changes, the changes need to be handled to not impact downstream processes.
- **Timely performance**: Raw data needs to be converted into actionable information within the shortest possible time. The expectations for data prep and delivery times must be transparent for both DW/BI team and users.
- **Security and privacy**: Access control to protect organizations confidential information.
- **Drive decision making**: Needs to have right data to support this process. Main Outputs: the decisions that are made based on the data.
- **Usage and adoption**:  No matter how well built the system is, it needs to be used to produce impact. Acceptance is also a test. Business users embrace simple and fast systems.

To maintain a DW/BI system over time, here is an overview of tips and responsibilities:

- **Understand your users**: Job, responsibilities, goals and objectives. Find out the decisions they want to make based on data. Find best users for making high impact decisions. Find new users and present them the system.
- **Make sure the data being delivered is correct, relevant and acessible**: Present the most robust and actionable data. User interfaces should be simple. Validate and monitor data accuracy and quality. Adapt the system to changes in business priorities and data availability.
- **Maintain the system**:Justify investiments by presenting decisions made using the system. Deliver regular updates. Maintain business users trust. Keep users, executives and tech teams happy.

## Dimensional Modelling

Dimensional modelling is the preferred technique for presenting analytic data because it addresses two problems:

1. Deliver understandable data to business users.
2. Deliver fast query performance.

Dimensional modelling has simple dimensional structure, which ensures users can easily understand the data, the software and navigate it to deliver quick results.

### Third Normal Form

- Dimensional models are often in relational database management systems (RDBMS), but not in the third normal form (3NF) which seeks to remove data redundancies.
- In 3NF data is divided in discrete entities, each of which become a relational table.
    - 1NF: A relation is in first normal form if every attribute in that relation is singled valued attribute.
    - 2NF: A relation that is in First Normal Form and every non-primary-key attribute is fully functionally dependent on the primary key, then the relation is in Second Normal Form (2NF).
    - 3NF: A relation that is in First and Second Normal Form and in which no non-primary-key attribute is transitively dependent on the primary key, then it is in Third Normal Form (3NF).
    - 2NF vs 3NF:
        - 2NF: No partial functional dependency of non-prime attributes are on any proper subset of candidate key is allowed.
        - 3NF: No transitive functional dependency of non-prime attributes on any super key is allowed. .
- These structure produce complex "spider web like" models.
- 3NF models are sometimes referred to as Entity Relationship diagrams (ER diagrams) which communicate relationships between tables.
- Both 3NF and dimensional models can be presented in ERDs, but the 3NF models are the degree of normalization (called normalized models by the book).
    - **Upside:** Immensely useful in operational processing because an update or insert touches the database in only one place.
    - **Downside:** Too complicated for BI queries. Users can't understand or navigate the model.
- Most RDBMS cant efficiently query a normalized model.
- Normalized models go against the basic definitions of DW/BI systems (simplicity and performance).
- We can build dimensional models which will contain the same information as a normalized model, but reorganize the data in a format that delivers understandability, query performance and adaptability.

### Star Schemas vs OLAP Cubes

- **Star schema:** Dimensional models in RDBMS are referred to star schemas because they resemble a star like structure.
- **OLAP cubes:** Dimensional models in multidimensional database environments are called online analytical processing (OLAP) cubes.
    - When data is loaded it is stored in an optimized format for dimensional data.
    - Aggregations or summary tables are created beforehand by the OLAP cube engine to optimize performance.
    - Upside:
        - Greater query performance because of optimizations.
        - Robust set of functions for analyticals needs which are better than traditional SQL.
        - More security options such as blocking access to detailed data but providing open access to summary data.
        - Slowly changing dimensional type 2 changes are supported, but requires reprocessing.
        - Support transaction and periodic snapshot fact tables, but doesn't handle accumulating snapshot fact tables
    - Downside:
        - Takes long to perform initial load (especially with large datasets).
        - Performance improvements haven't made much difference in comparison to advances in computer hardware.
        - Varies more from OLAP vedor to vendor. More difficult to port.

Both of these are dimensional models, however, the physical implementation differs. It's recommended by the book to first store detailed, atomic information into star schema, and the populate an OLAP cube from the star schema.

### Fact Tables

Returning back to star schemas:

**Fact table:** entity in a dimensional model that stores the performance measurements resulting from an organizations business process events.

- Dimensional model becomes centralized repository for each set of measurements.
- 1 measured event = 1 new row in fact table = Grain of the table.
- Only register events that happened (don't fill with zeros).
- Should make up 90% of the storage consumed by a dimensional model (so don't replicate them).
- Should have a few columns and lots of rows.
- Has two or more foreign keys that connect to the dimension tables' primary keys.
- Its primary key is the composition of all the foreign keys (normally called a composite key).

**Fact:** a business measure.
- Normally continuously valued. Normally a discrete list of values.
- The most useful facts are numeric and additive (e.g dollar sales amount).
- **Semi additive facts:** Cannot be summed across the time dimension (e.g account balance).
- **Non additive facts:** Can never be added (e.g unit price).
- These types of facts require using counts, averages or individual analyses.
- Crutial BI applications rarely retrieve a single fact table row.
- Millions of fact rows are processed at a time, and the most useful thing to do is aggregate them.
- **Atomic data:** Data that has not been aggregated, with the most dimensionality.
- These tables should always contain atomic data, so that users can ask the data whatever question they want.
    

### Dimension Tables

Dimension tables are the companions to a fact table. These tables contained the textual context associated with a business process measurement event.

- Who, what, where, when how and why associated with an event.
- Normally have many columns and many attributes.
- Normally have fewer rows than fact tables, but can be wide with many large text columns.
- Defined by a single primary key.
- The attributes should be a primary source of query constraints, groupings and report labels.
- Critical for making DW/BI system usable and understandable
- Attributes should use real words instead of cryptic abbreviations (decode and describe them).
- Numerical data may be a fact or dimension attribute. Numerical attributes should be considered dimensional attributes if they are discrete and constant.
- **Snowflaking:** Normalizing data so that all of the dimensional attributes end up becoming separate dimensions (3FN)
    - Dimensional tables are normally highly denormlized with flattened many to one relationships within a single dimension table.
    - Since these tables are usually small, normalizing doesn't improve performance/storage that much.
    - Dimensional table space should be traded of for simplicity and accessibility.

### Star Schema

Each business process is a dimensional model that consists of a fact table containing numeric measurements surrounded by dimension tables that contain the textual context for each event. 

**Star Join:** Star Like structure that associates a fact table with the dimensional tables.

![Star schema example](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_1.png?raw=true)

Benefits for this model are:

- Highly recognizable design for business users.
- Reduced number of tables and useful business descriptors make it easy to explore the data.
- Database optimizers process queries with fewer joins more efficiently.
- Column change: New dimensions can be added as long a single value can be added for each row of the fact table.
- Row change: New facts can easily be added to the fact table as long as the new fact contains the same details that the fact table requires by performing `INSERT`s.
- Dimension attribute change: New attributes can be added to further improve analysis possibilities with `ALTER TABLE`.

## Kimball's DW/BI Architecture

In Kimball's architecture, there are four separate and distinct components to consider for a DW/BI system: Operational Source Systems, ETL System, Data Presentation Area and Business Intelligence Applications.

![Kimball DW/BI Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_2.png?raw=true)

### Operational Source Systems

Operational systems of records that capture business transactions. 

- Normally outside the warehouse (little control over content and format).
- Made for processing performance and availability.
- Queries are one row at a time, restricted, simple.
- Little historical data.

### ETL System

- **ETL:** Extract, transform and load. Has work area, data structures and processes.
- **Extraction Step:** Reading and understanding the source data and copying the data needed into the ETL system for staging. Here the data belongs to the data warehouse. Ready for further manipulation
- **Transformation Step:** Cleaning the data (correct misspellings, resolving domain conflicts, fill in missing values, parse data to correct formats, etc). Combining data from multiple sources. Deduplicate data. Create metadata for improving data quality overtime.
- **Load Step:** Physical loading of data into the presentation areas target dimensional models. ETL output is to fit the data into the dimension and fact tables. Can include surrogate key assignments, splitting or combining columns, and joining normalized data into normalized dimensions and validating the outputs. Notify business community that new data has been published.
- Normalized databases can exist within an ETL system, but this is not the end goal since normalized structures make queries hard and make performance worse.

### Data Presentation Area

Where data is structured, stored and made available for querying by end users, report writers and other BI applications.

- Business users don't interact with the ETL system.
- Should use dimensional schemas (star schemas or OLAP cubes) since we have BI users.
- Must contain detailed and atomic data (not summary/aggregated data) so that we can answer very complex questions/queries. Aggregated data can be used for performance reasons, however, this it's unnacceptable that this is the only data stored.
- Reports should be populated from shared tables between multiple teams.
- Dimensional structures should use common, conformed dimensions (shared between fact tables). The users must be able to tie different data sets together

### Business Intelligence Applications

BI: Range of capabilities provided to business users to leverage the presentation area for analytical decision making. Can be simple or complex, ranging from  an ad hoc query tool to a data mining or modelling application. Some applications may even upload results back into operational source systems, ETL system or presentation area (Refered to reverse ETL in recent bibliography).

## Alternative DW/BI Architectures

There are other architectural approaches to designed DW/BI systems. One thing to note is that over time the differences between Kimballs' architecture and these other architectures have become less distinct. 

### Indepedent Data Mart

Analytic data is deployed on a departmental basis, with no concern for sharing and integrating information across the enterprise.

- Data is extracted from the operational source system processes.
- Construction of a database to satisfy needs of the current department, reflecting business rules and preferred labelling. This data mart only addresses the analytical needs for this department.
- Another department may be interested in the same source data, but their data mart will be built for them, constructing a simular structure but addressing its own needs.
- Advantages: Indepent data marts use dimensional modelling so that data is easy to use. Development costs are low due to simple architecture (since sylos don't need to comunicate and be consistent)..
- Disadvantages: Incosistency for data and metrics between different deparments. Inefficient and wasteful in the long run.

![Indepent Data Mart Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_3.png?raw=true)

### Inmon Architecture / Hub-and-Spoke Corporate Information Factory (CIF)

- **Data Aquisition**: ETL System for extracting and processing datas from operational systems.
- **Enterprise Data Warehouse (EDW)**: 3NF database containing atomic data produced through data acquisition.
- Common for business users to access the EDW due to level of detail or timeliness of data.
- Subsequent ETL data delivery processes deliver data to downstream reporting and analytic environments.
- Data presentation is normally a dimensional model, departmental centric (business centric in Kimball architecture) and populated with aggregated data (atomic data in Kimball architecture)
- Can be hard to join presentation data to EDW data due to manipulations.

![Inmon Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_4.png?raw=true)

### Hybrid Inmon/Kimball Architecture

- This architecture populates a Inmon based EDW that is off limits to users for analytics and reporting.
- EDW is a source for Kimball based presentation area in which data is dimensional, atomic, complemented by aggregates, process centric and conforms to the enterprise data warehouse bus architecture.
- If money has been invested in creating a 3NF EDW, but it doesn't deliver fast and flexible reporting, this hybrid approach may be appropriate.
- If starting from scratch, the multiple ETL processes and replicated atomic data storage may cost more to develop and operate.

![Hybrid Inmon/Kimball Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_5.png?raw=true)

## Data Modelling Myths

1. **For summary data only**: Summary data may be provided to complement granular detail and improve performance for common queries, but data in a dimensional model should be atomic. Also, nothing about dimensional modelling limits data history, but it's generally cut off by business requirements.
2. **Departmental data, not enterprise**: Dimensional models should be organized around business processes. Multiple departments may want to perform similar analysis for the same process, and extracting the same data multiple times may create departmental silos which cause incosistencies.
3. **Not scalable**: Fact tables frequently have billions of rows. Both normalized and dimensional models contain the same information and data relationships, what changes is the organization.
4. **Limited to predictable usage**: Dimensional model design should be business measure centric, indepedente of the use case. It's important to consider BI requirements, but reports change over time. Dimensional models can handle change gracefully. Atomic data is the key to flexibility.
5. **Doesn't integrate**: Dimensions can be maintained as centralized, persistent master data in the ETL system and reused for many dimensional models to ensure data integration and consistency. This requires organizational consensus on standardized labels, values and defitions however.
