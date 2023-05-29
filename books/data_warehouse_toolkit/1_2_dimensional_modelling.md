# Dimensional Modelling

Dimensional modelling is the preferred technique for presenting analytic data because it addresses two problems:

1. Deliver understandable data to business users.
2. Deliver fast query performance.

Dimensional modelling has a simple dimensional structure, which ensures users can easily understand the data, the software and navigate it to deliver quick results.

## Third Normal Form

- Dimensional models are often in relational database management systems (RDBMS), but not in the third normal form (3NF) which seeks to remove data redundancies.
- In 3NF data is divided into discrete entities, each of which becomes a relational table.
    - 1NF: A relation is in first normal form if every attribute in that relation is single-valued attribute.
    - 2NF: A relation that is in First Normal Form and every non-primary-key attribute is fully functionally dependent on the primary key, then the relation is in Second Normal Form (2NF).
    - 3NF: A relation that is in First and Second Normal Form and in which no non-primary-key attribute is transitively dependent on the primary key, then it is in Third Normal Form (3NF).
    - 2NF vs 3NF:
        - 2NF: No partial functional dependency of non-prime attributes are on any proper subset of candidate key is allowed.
        - 3NF: No transitive functional dependency of non-prime attributes on any super key is allowed. .
- These structures produce complex "spider web-like" models.
- 3NF models are sometimes referred to as Entity Relationship diagrams (ER diagrams) which communicate relationships between tables.
- Both 3NF and dimensional models can be presented in ERDs, but the 3NF models are the degree of normalization (called normalized models by the book).
    - **Upside:** Immensely useful in operational processing because an update or insert touches the database in only one place.
    - **Downside:** Too complicated for BI queries. Users can't understand or navigate the model.
- Most RDBMS cant efficiently query a normalized model.
- Normalized models go against the basic definitions of DW/BI systems (simplicity and performance).
- We can build dimensional models which will contain the same information as a normalized model, but reorganize the data in a format that delivers understandability, query performance and adaptability.

## Star Schemas vs OLAP Cubes

- **Star schema:** Dimensional models in RDBMS are referred to star schemas because they resemble a star-like structure.
- **OLAP cubes:** Dimensional models in multidimensional database environments are called online analytical processing (OLAP) cubes.
    - When data is loaded it is stored in an optimized format for dimensional data.
    - Aggregations or summary tables are created beforehand by the OLAP cube engine to optimize performance.
    - Upside:
        - Greater query performance because of optimizations.
        - Robust set of functions for analytical needs which are better than traditional SQL.
        - More security options such as blocking access to detailed data but providing open access to summary data.
        - Slowly changing dimensional type 2 changes are supported but require reprocessing.
        - Support transaction and periodic snapshot fact tables, but doesn't handle accumulating snapshot fact tables
    - Downside:
        - Takes a long time to perform the initial load (especially with large datasets).
        - Performance improvements haven't made much difference in comparison to advances in computer hardware.
        - Varies more from OLAP vendor to vendor. More difficult to port.

Both of these are dimensional models, however, the physical implementation differs. It's recommended by the book to first store detailed, atomic information into a star schema, and then populate an OLAP cube from the star schema.

## Fact Tables

Returning back to star schemas:

**Fact table:** entity in a dimensional model that stores the performance measurements resulting from an organizations business process events.

- Dimensional model becomes a centralized repository for each set of measurements.
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
- Crucial BI applications rarely retrieve a single fact table row.
- Millions of fact rows are processed at a time, and the most useful thing to do is aggregate them.
- **Atomic data:** Data that has not been aggregated, with the most dimensionality.
- These tables should always contain atomic data so that users can ask the data whatever question they want.
    

## Dimension Tables

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
    - Dimensional tables are normally highly denormalized with flattened many-to-one relationships within a single dimension table.
    - Since these tables are usually small, normalizing doesn't improve performance/storage that much.
    - Dimensional table space should be traded off for simplicity and accessibility.

## Star Schema

Each business process is a dimensional model that consists of a fact table containing numeric measurements surrounded by dimension tables that contain the textual context for each event. 

**Star Join:** Star Like structure that associates a fact table with the dimensional tables.

![Star schema example](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/images/1_1.png?raw=true)

Benefits for this model are:

- Highly recognizable design for business users.
- Reduced number of tables and useful business descriptors make it easy to explore the data.
- Database optimizers process queries with fewer joins more efficiently.
- Column change: New dimensions can be added as long as a single value can be added for each row of the fact table.
- Row change: New facts can easily be added to the fact table as long as the new fact contains the same details that the fact table requires by performing `INSERT`s.
- Dimension attribute change: New attributes can be added to further improve analysis possibilities with `ALTER TABLE`.

## Reference

Personal notes for educational purposes based on the book [The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) by Ralph Kimball and Margy Ross, 3rd edition.
