import requests
import duckdb
import json
import pandas as pd




class RetailSalesETL:
    """
    This class is used to mock an ETL process for the retail sales model.
    """
    def __init__(self, db):
        self.db = db
        self._MOCKAROO_API_KEY = ""

    # Populate store_dim table
    def populate_store_dim(self, table_name="store_dim", n=3):
        fields = [{"store_id":i, "store_name": f"Store {i}" } for i in range(n)]
        df = pd.DataFrame(fields)
        self.db.execute(f"TRUNCATE TABLE {table_name};")
        self.db.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
        self.db.commit()

    # Populate promotion_dim table
    def populate_promotion_dim(self, table_name="promotion_dim"):
        fields = [
            {"promotion_id":1, "promotion_type": "No promotion"},
            {"promotion_id":2, "promotion_type": "Coupon"},
            {"promotion_id":3, "promotion_type": "Discount"},
        ]
        df = pd.DataFrame(fields)
        self.db.execute(f"TRUNCATE TABLE {table_name};")
        self.db.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
        self.db.commit()

    # Populate the payment_method_dim
    def populate_payment_method_dim(self, table_name="payment_method_dim"):
        fields = [
            {"payment_method_id":1, "payment_method": "Cash"},
            {"payment_method_id":2, "payment_method": "Debit Card"},
            {"payment_method_id":3, "payment_method": "Credit Card"},
        ]
        df = pd.DataFrame(fields)
        self.db.execute(f"TRUNCATE TABLE {table_name};")
        self.db.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
        self.db.commit()

    # Populate cashier_dim table
    def populate_cashier_dim(self, n=2, table_name="cashier_dim"):
        # Define fields that need to be populated
        fields = [
            {
                "name": "cashier_id",
                "type": "Row Number"
            },
            {
                "name": "cashier_name",
                "type" :"Full Name"
            }
        ]

        # Make a GET request to the API
        url = f"https://api.mockaroo.com/api/generate?key={self._MOCKAROO_API_KEY}&count={n}&fields={json.dumps(fields)}&seed=1"
        data = requests.get(url).json()
        df = pd.DataFrame(data)

        # Create the store_dim table if it doesn't exist
        self.db.execute(f"TRUNCATE TABLE {table_name};")
        self.db.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
        self.db.commit()

    # Populate product_dim table
    def populate_product_dim(self, n=5, table_name="product_dim"):
        # Define fields that need to be populated
        fields = [
            {
                "name": "product_id",
                "type": "Row Number"
            },
            {
                "name": "product_name",
                "type" :"Product (Grocery)"
            }
        ]

        # Make a GET request to the API
        url = f"https://api.mockaroo.com/api/generate?key={self._MOCKAROO_API_KEY}&count={n}&fields={json.dumps(fields)}&seed=1"
        data = requests.get(url).json()
        df = pd.DataFrame(data)

        # Create the store_dim table if it doesn't exist
        self.db.execute(f"TRUNCATE TABLE {table_name};")
        self.db.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
        self.db.commit()

    def populate_date_dim(self, table_name="date_dim", n=3):
        import datetime as dt

        # Generate list of N dates after min_date, one day increment
        min_date = dt.datetime(2023, 3, 1)
        dates = [min_date + dt.timedelta(days=x) for x in range(n)]

        # format dates into strings
        dates = [date.strftime("%Y-%m-%d") for date in dates]

        fields = [{"date_id":i, "date_value": d } for i,d in enumerate(dates)]
        df = pd.DataFrame(fields)
        self.db.execute(f"TRUNCATE TABLE {table_name};")
        self.db.execute(f"INSERT INTO {table_name} SELECT * FROM df;")
        self.db.commit()

    # Populate the fact table
    def populate_retail_sales(self, table_name="retail_sales"):
        # Truncate the table before inserting data
        self.db.execute(f"TRUNCATE TABLE {table_name};")

        # Select random value combinations from the dimension tables
        self.db.execute(f"""
        INSERT INTO {table_name}
        (store_id, promotion_id, payment_method_id, cashier_id, product_id, date_id, sales_quantity, regular_unit_price, cost_unit_price, discount_unit_price, pos_transaction_id)
        WITH q_raw AS (
            SELECT
                store_id,
                promotion_id,
                payment_method_id,
                cashier_id,
                product_id,
                date_id,
                ROUND((RANDOM() * 9) + 1, 0) AS sales_quantity,
                ROUND(RANDOM() * 10, 2) AS regular_unit_price,
            FROM
                store_dim,
                promotion_dim,
                payment_method_dim,
                cashier_dim,
                product_dim,
                date_dim
            ORDER BY RANDOM()
            LIMIT 50
        ), 
        q_cost AS (
            SELECT 
                *,
                ROUND( regular_unit_price * ( 0.5 + ( 0.25 * RANDOM())), 2) AS cost_unit_price
            FROM q_raw
        )
        SELECT
            store_id, 
            promotion_id, 
            payment_method_id, 
            cashier_id, 
            product_id, 
            date_id, 
            sales_quantity, 
            regular_unit_price, 
            cost_unit_price,
            (CASE 
                WHEN promotion_id > 1 
                -- limit discount to 25 percent of original price
                THEN ROUND(cost_unit_price * (RANDOM() * 0.24 + 0.01) , 2)
                ELSE 0 
            END) AS discount_unit_price,
            ROW_NUMBER() OVER () AS pos_transaction_id
        FROM q_cost;
        """)
        self.db.commit()

    def load_retail_sales_data(self):

        self.populate_store_dim()
        self.populate_promotion_dim()
        self.populate_payment_method_dim()
        self.populate_cashier_dim()
        self.populate_product_dim()
        self.populate_date_dim()
        self.populate_retail_sales()