
# Common DW/BI Architectures

## Kimball's DW/BI Architecture

In Kimball's architecture, there are four separate and distinct components to consider for a DW/BI system: Operational Source Systems, ETL System, Data Presentation Area and Business Intelligence Applications.

![Kimball DW/BI Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_2.png?raw=true)

### Operational Source Systems

Operational systems of records that capture business transactions. 

- Normally outside the warehouse (little control over content and format).
- Made for processing performance and availability.
- Queries are one row at a time, restricted and simple.
- Little historical data.

### ETL System

- **ETL:** Extract, transform and load. Has work area, data structures and processes.
- **Extraction Step:** Reading and understanding the source data and copying the data needed into the ETL system for staging. Here the data belongs to the data warehouse. Ready for further manipulation
- **Transformation Step:** Cleaning the data (correct misspellings, resolving domain conflicts, filling in missing values, parse data to correct formats, etc). Combining data from multiple sources. Deduplicate data. Create metadata for improving data quality over time.
- **Load Step:** Physical loading of data into the presentation areas target dimensional models. ETL output is to fit the data into the dimension and fact tables. This can include surrogate key assignments, splitting or combining columns, joining normalized data into normalized dimensions and validating the outputs. Notify the business community that new data has been published.
- Normalized databases can exist within an ETL system, but this is not the end goal since normalized structures make queries hard and make performance worse.

### Data Presentation Area

Where data is structured, stored and made available for querying by end users, report writers and other BI applications.

- Business users don't interact with the ETL system.
- Should use dimensional schemas (star schemas or OLAP cubes) since we have BI users.
- Must contain detailed and atomic data (not summary/aggregated data) so that we can answer very complex questions/queries. Aggregated data can be used for performance reasons, however, it's unacceptable that this is the only data stored.
- Reports should be populated from shared tables between multiple teams.
- Dimensional structures should use common, conformed dimensions (shared between fact tables). The users must be able to tie different data sets together

### Business Intelligence Applications

BI: Range of capabilities provided to business users to leverage the presentation area for analytical decision-making. Can be simple or complex, ranging from an ad-hoc query tool to a data mining or modelling application. Some applications may even upload results back into operational source systems, ETL systems or presentation areas (Referred to as reverse ETL in recent bibliography).

## Alternative DW/BI Architectures

There are other architectural approaches to designing DW/BI systems. One thing to note is that over time the differences between Kimballs' architecture and these other architectures have become less distinct.

### Indepedent Data Mart

Analytic data is deployed on a departmental basis, with no concern for sharing and integrating information across the enterprise.

- Data is extracted from the operational source system processes.
- Construction of a database to satisfy the needs of the current department, reflecting business rules and preferred labelling. This data mart only addresses the analytical needs of this department.
- Another department may be interested in the same source data, but their data mart will be built for them, constructing a similar structure but addressing its own needs.
- Advantages: Independent data marts use dimensional modelling so that data is easy to use. Development costs are low due to simple architecture (since silos don't need to communicate and be consistent).
- Disadvantages: Inconsistency for data and metrics between different departments. Inefficient and wasteful in the long run.

![Indepent Data Mart Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_3.png?raw=true)

### Inmon Architecture / Hub-and-Spoke Corporate Information Factory (CIF)

- **Data Aquisition**: ETL System for extracting and processing data from operational systems.
- **Enterprise Data Warehouse (EDW)**: 3NF database containing atomic data produced through data acquisition.
- Common for business users to access the EDW due to the level of detail or timeliness of data.
- Subsequent ETL data delivery processes deliver data to downstream reporting and analytic environments.
- Data presentation is normally a dimensional model, departmental-centric (business-centric in Kimball architecture) and populated with aggregated data (atomic data in Kimball architecture)
- Can be hard to join presentation data to EDW data due to manipulations.

![Inmon Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_4.png?raw=true)

### Hybrid Inmon/Kimball Architecture

- This architecture populates an Inmon-based EDW that is off-limits to users for analytics and reporting.
- EDW is a source for Kimball-based presentation area in which data is dimensional, atomic, complemented by aggregates, process-centric and conforms to the enterprise data warehouse bus architecture.
- If money has been invested in creating a 3NF EDW, but it doesn't deliver fast and flexible reporting, this hybrid approach may be appropriate.
- If starting from scratch, the multiple ETL processes and replicated atomic data storage may cost more to develop and operate.

![Hybrid Inmon/Kimball Architecture](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_5.png?raw=true)

## Data Modelling Myths

1. **For summary data only**: Summary data may be provided to complement granular detail and improve performance for common queries, but data in a dimensional model should be atomic. Also, nothing about dimensional modelling limits data history, but it's generally cut off by business requirements.
2. **Departmental data, not enterprise**: Dimensional models should be organized around business processes. Multiple departments may want to perform similar analyses for the same process, and extracting the same data multiple times may create departmental silos which cause inconsistencies.
3. **Not scalable**: Fact tables frequently have billions of rows. Both normalized and dimensional models contain the same information and data relationships, what changes is the organization.
4. **Limited to predictable usage**: Dimensional model design should be business measure centric, independent of the use case. It's important to consider BI requirements but reports change over time. Dimensional models can handle change gracefully. Atomic data is the key to flexibility.
5. **Doesn't integrate**: Dimensions can be maintained as centralized, persistent master data in the ETL system and reused for many dimensional models to ensure data integration and consistency. This requires organizational consensus on standardized labels, values and definitions however.

## Reference

Personal notes for educational purposes based of the book [The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) by Ralph Kimball and Margy Ross, 3rd edition.
