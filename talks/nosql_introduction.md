# Introduction to NoSQL Databases - Martin Fowler

## History

### Mid 80s

- Rise of relational databases
- Benefits: 
	- Data Persistence
	- concurrency with transactions,
	- Standard database language (SQL)
	- Great for integration and reporting
- Problems:
	- Impedance mismatch: Memory structure vs Database structure. 
	- Leads to object to relational mapping frameworks.

### Mid 90s: 

- Rise of object databases.
- Integration with relational databases made it hard for object databases to catch on.

### Mid 2000s

- Relational kept its dominance (especially in the enterprise space).
- Rise of internet and sites with lots of traffic
- Vertical scaling became a problem (expensive and with hard limitations).
- SQL was designed for Vertical scaling.
- Big data players had a hard time performing horizontal scaling with relational databases.

## NoSQL Common Characterists

- Non-relation
- Open source
- Supports horizontal scaling (Cluster-friendly)
- 21st Century web 
- Schema-less

## Common data models

### Key value Store

- You have a key
- You provide the key to the database
- You grab the value of the key
- The value could be anything (document, image, number)
- A hash map but persistant.
- Metadata can be stored about the values (similar to document)

### Document

- Thinks of database as storage of documents
- Each document is a complex data structure
- Normally uses JSON for data representation
- You can query document structure and retrive/update portions of the document
- Doesn't tend to have a set schema (Common pattern of NoSQL)
	- Very flexible but has problems
	- Normally an implicit schema is derived
	- This schema needs to be managed and tracked
	- Schemaless is a bad term
	- Very flexible, but ther is an implicit schema
- Normally there is an ID for the document - and this is the same as the key in a key-value store

### Column N

- Row-key can store multiple column families
- Each column family is a combination of columns
- Columns can be adressed by combining row key and column name.
- More complex data model
- Retriavel is easier because of named columns

### Graph

- Uses different data model to aggregate orientation
- Node and Arc graph structure
- Very good at handling relantionships
- Relational databases require joins, foreign keys, doesn't scale too well
- Easy and optimized for getting diferent relations
- Separate query language for complex querying (very difficult to write in SQL) which is very optimized
- Graph oriented databases breaks data into smaller units instead of cumpling them together

## Aggregate oriented databases

- Definition: Some single unit is stored within the database.
- Examples of aggregate oriented databases = Key value, document store and column N
	- Aggregate for KV - Value;
	- Aggregate for Document - Document
	- Aggregate for column N - Column Family
- The whole object can be stored within the database without ORM
	- This is useful for distributing data across clusters
	- The aggregate tells us what data needs to be placed together
- Restructuring relations with aggregate oriented databases is complicated
- Aggregate oriented is good when the same aggregate is used to read/write data.
- It's bad if we want to slice and dice data
- Can handle relationships, but can be limited or messy.

## NoSQL and Consistency

- Relational databases are ACID compliant
- NoSQL doesn't do this
- We can have problems where part of the data is written and that incomlpete information is read
- Also can have problems where parts of data are overwritten
- Need to have a mechanism for atomic updates
- Graph databases tend to follow ACID updates
- Aggregate databases are ACID in single aggregates

### Logical Consistancy
- To prevent write write conflicts, GET and POST for data must be a single transaction.
	- This is hard to do since transactions must be short.
	- Only possible with low performance needs.
	- Alternative is to only set the update as transaction
		- This avoids collision for different transaction data being present in different tables
		- We still have a conflict - two people made updates without knowing the content of the other person
		- If more than one aggregate nees to be modified - this could also cause incosistencies
	- This can be solved with an offline lock
		- Each aggregate is given a version stamp.
		- When its retrieved, you bring the version stamp together
		- When its posted - we compare the version stamp
		- First person gets and post ok
		- Second person gets an error on post - and the error is treated
- Up we've analysed logical consistancy
	- Occurs on one or multiple machines

### Distribution

- Distributed data can be:
	- Sharded: Taking one copy of the data and putting in different machine
		- Each data lives only on one machine
		- Logical incosistancy still happens
	- Replication: Same data on different machines 
		- Good for performance since more nodes can handle the same request
		- Good for resiliance so that if any nodes go down, the others can take over
		- New problem emerges - communication between nodes when conflicts emerge between nodes
		- Also the communication between nodes may fail
			- The system may disable any requests - this keep consistency
			- An alternative may be accepting both requests - this guarantees availability
			- This behaviour is a choice - decided by domain (business)

### CAP Theorem

- Consistency, Availability, PartitionTolerance - Pick 2
- A better way to state this: You have partitioning (distributed) - Pick Availability or consistency.
- This is actually a spectrum - we can choose varying degrees of availability/cosistency.
- Most of the time we're trading off cosistency vs response time.
- Its up to the business to decide these tradeoffs - not tech teams.

### Other topics to explore

- Relaxing durability
- Eventual consistency
- Quorums
- Read you writes cosistency

## When to use NoSQL

### Large Scale Data

- Most of the time, NoSQL is better for processing big ammounts of data
- Distributed relational databases are hard to get right
- Question: Most companies don't need this type of scale
	- Reality: Lots of data is being generated
	- Every organization is going to be capturing more and more data
	- The problem will grow

### Easier Development

- Most people actually prefer easier development
- Comapnies normally have natural aggregates
- Working with aggregates is easier for companies
- Impedance mismatch is alot less of a problem with natural aggregates
- Most companies can't map their data to a relational databases (well), so they assume NoSQL is better
- You simplify the problem by using NoSQL

### Integration Problem

- Object databases went away because of dificulties with database integration
- Currently, most companies have a web service that communicates with databases
- Integration isn't done directly with the database, So encapsulation simplifies the problem

### Analytics

- Normally Data warehousing is sold by a marketer that promises data centralization
- Most of these projects go badly
- Graph Databases are great for graph analytics
- Aggregate databases can store large quantities of data


## Conclusion

- Will NoSQL be the future of databases?
- Probably not
- Polyglot Persistance: Room for lots of kind of databases
- Relational databases will still play a big role
- An application may use lots of different databases
- An organization will definitaly use lots of databases
- The database will selected based on the nature of the problem
- Problems
	- Need to decide what database is appropriate
	- Organizational Change - DBAs will not like the change
	- NoSQL datbases are immature - don't have tools and experience we have with relational databases
	- Consistency can still be a problem
- Analyse type of project when choosing NoSQL
	- Fast time to market
	- Very data intensive project
	- Is it a strategic project - than time to market is important and NoSQL may help
	- If it's a simple, auxiliary project - It might not make sense to use NoSQL

## Complementary reads

- NoSQL: A Brief Guide to the Emerging World of Polyglot Persistence Disilled - Pramodkumar J Sadalage & Martin Fowler. 
- [NoSQL Databases](https://martinfowler.com/data/index.html#nosql)
