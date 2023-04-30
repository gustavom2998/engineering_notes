# Dimensional modelling 

## Business requirements 

- Understand the business by talking to business representatives. 
    - What are the KPIs?
    - What are some business issues that need to be solved with data?
    - What analytical needs will be supported by this model

## Data realities

- Talk with source systems experts to understand 
    - The type of data that is available.
    - How often the models change.
    - What systems is the data coming from and how is it stored.
    - Common problems with it.
    - How often it's updated.

## Collaborative modelling workshops

- Dimensional models should be design with help from experts and data governance representatives from the business.
- The model should be derived from a interactive workshops with these experts.
- Models shouldn't be designed in isolation since the designer may not understand the business requirements or the data realities.

## Four step design process

1. Select the business process
    - Identify operational activities to be modeled.
    - Identify events that capture performance metrics (for fact table).
    - Each process is a row in the enterprise data warehouse bus matrix.
2. Declare the grain
    - Establish a contract on what a single fact table row represents.
    - Facts/dimensions must be consistent with the grain.
    - Each grain = a separate physical table.
3. Identify the dimensions
    - Who, what, where, when, why, how.
    - Must contain descriptive attributes used by BI applications for filters.
4. Identify the facts
    - 1 fact = 1 process events. 
    - Measure values are almost always numeric.
    - List facts consistent with the table grain.
    - After meeting business requirements, adapt to data realities.

## Case study: Retail Sales

**Context**: Large grocery chain. Multiple stores spread out across multiple states. Each store has multiple departments: Grocery, frozen foods, meats, product, bakery, floral, health/beauty. Multiple products identified by Stock Keep units (SKU).

**Data collection**: Several operational systems. Cash registers collect customer purchases, Point of Sale systems collect data related to SKUs. Customer receipts contain a copy of: Store number, cashier identifier and name, product SKU, product name, cost, discount information, coupon information, total cost, item count, transaction number, transaction time and a receipt number. Vendor deliveries are also tracked at store back door.

**Business interests**: Logistics of ordering, stocking and selecting products while maximizing profits. This comes from charging as much as possible for products while keeping customers happy. Management and marketing makes decisions related to pricing and promotions which can greatly impact sales. Promotions include temporary price reductions, coupons and ads.

1. Business processes: Better understand point of sale systems (retail sales transactions). The objective is to analyze **what products** are selling, in **what stores**, with **what promotions** and **when**.
2. Grain: When we analyze the businness process we proposed to analyze, we seen that the grain is a **single product in a sales transaction**. After analyzing the proposal, we can see that we don't propose drilling down deeper than into an individual products in a sale.
3. Dimensions: There are some keywords that have repeated over our analysis. **Stores**, **products**, **transactions**, **promotions**, **cashiers**, **payment methods** and **dates**.
4. Facts: We can basically identify how to transform the grain into a table. The grain is a single product in a sales transaction. The facts are metrics collected for the grain, therefore we can identify some metrics from the receipt: Number of products, regular price, discount, extended discount (quantity * discount), extended sales dollar amount (quantity * net unit price), net paid price(sales dollar - extended discount). Also some systems contain a standard dollar cost price.