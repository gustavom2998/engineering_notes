# The Data Warehouse Toolkit

Personal notes for educational purposes based of the book [The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling](https://www.amazon.com/Data-Warehouse-Toolkit-Definitive-Dimensional/dp/1118530802) by Ralph Kimball and Margy Ross. I also took some time to simplify some diagrams to go along with the notes. The notes are based of the 3rd edition of the book. The notes should only be used for In the near future, I'll try to add some SQL samples to the notes.

## Book Notes

- [Chapter 1: Data Warehouseing and Bussiness Intelligence Introduction](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/1_1_dw_bi_introduction.md)
- [Chapter 1: Dimensional Modelling](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/1_2_dimensional_modelling.md)
- [Chapter 1: Common DW/BI Architecures](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/1_3_dw_architectures.md)
- [Chapter 2: Dimensional modelling concepts - Four step design process](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/2_1_dm_four_steps.ipynb)
- [Chapter 2: Fact Table Techniques - Measure Categories](https://github.com/gustavom2998/engineering_notes/blob/main/books/data_warehouse_toolkit/2_2_fact_measure_categories.ipynb)
- 

## Personal Notes

I started reading this book in November 2021. The context for getting into this book was that I was half way into attempting to structure raw data from our data lake and my manager mentioned it might be a good read. He was right, the book gave me a recipe for doing the stuff I had been doing for the last couple of months without understanding what I was doing or why I was doing it.

We ended up not implementing a dimensional model, we only got up to creating a 3NF Model for the ETL system and then had to settle for a one-big table solution. I managed to get a good grasp of needing to collect and transform data from multiple sources, needing to create metadata and consistent labels - and had first hand experience with the problems that came with it.

## Tools Used

- [Excalidraw](https://excalidraw.com): For drawing processes.
- [diagrams.net](https://app.diagrams.net): For drawing models.
- [Python/Jupyter Notebooks](https://jupyter.org): For combining notes with executable code.
- [DuckDB](https://duckdb.org): OLAP DBMS for testings ideas.