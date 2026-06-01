import pandas as pd
import numpy as np
import os
import time
import dotenv
import ast
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from typing import Dict, List, Union
from sqlalchemy import create_engine, Engine

# Create an SQLite database
db_engine = create_engine("sqlite:///munder_difflin.db")

# List containing the different kinds of papers 
paper_supplies = [
    # Paper Types (priced per sheet unless specified)
    {"item_name": "A4 paper",                         "category": "paper",        "unit_price": 0.05},
    {"item_name": "Letter-sized paper",              "category": "paper",        "unit_price": 0.06},
    {"item_name": "Cardstock",                        "category": "paper",        "unit_price": 0.15},
    {"item_name": "Colored paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Glossy paper",                     "category": "paper",        "unit_price": 0.20},
    {"item_name": "Matte paper",                      "category": "paper",        "unit_price": 0.18},
    {"item_name": "Recycled paper",                   "category": "paper",        "unit_price": 0.08},
    {"item_name": "Eco-friendly paper",               "category": "paper",        "unit_price": 0.12},
    {"item_name": "Poster paper",                     "category": "paper",        "unit_price": 0.25},
    {"item_name": "Banner paper",                     "category": "paper",        "unit_price": 0.30},
    {"item_name": "Kraft paper",                      "category": "paper",        "unit_price": 0.10},
    {"item_name": "Construction paper",               "category": "paper",        "unit_price": 0.07},
    {"item_name": "Wrapping paper",                   "category": "paper",        "unit_price": 0.15},
    {"item_name": "Glitter paper",                    "category": "paper",        "unit_price": 0.22},
    {"item_name": "Decorative paper",                 "category": "paper",        "unit_price": 0.18},
    {"item_name": "Letterhead paper",                 "category": "paper",        "unit_price": 0.12},
    {"item_name": "Legal-size paper",                 "category": "paper",        "unit_price": 0.08},
    {"item_name": "Crepe paper",                      "category": "paper",        "unit_price": 0.05},
    {"item_name": "Photo paper",                      "category": "paper",        "unit_price": 0.25},
    {"item_name": "Uncoated paper",                   "category": "paper",        "unit_price": 0.06},
    {"item_name": "Butcher paper",                    "category": "paper",        "unit_price": 0.10},
    {"item_name": "Heavyweight paper",                "category": "paper",        "unit_price": 0.20},
    {"item_name": "Standard copy paper",              "category": "paper",        "unit_price": 0.04},
    {"item_name": "Bright-colored paper",             "category": "paper",        "unit_price": 0.12},
    {"item_name": "Patterned paper",                  "category": "paper",        "unit_price": 0.15},

    # Product Types (priced per unit)
    {"item_name": "Paper plates",                     "category": "product",      "unit_price": 0.10},  # per plate
    {"item_name": "Paper cups",                       "category": "product",      "unit_price": 0.08},  # per cup
    {"item_name": "Paper napkins",                    "category": "product",      "unit_price": 0.02},  # per napkin
    {"item_name": "Disposable cups",                  "category": "product",      "unit_price": 0.10},  # per cup
    {"item_name": "Table covers",                     "category": "product",      "unit_price": 1.50},  # per cover
    {"item_name": "Envelopes",                        "category": "product",      "unit_price": 0.05},  # per envelope
    {"item_name": "Sticky notes",                     "category": "product",      "unit_price": 0.03},  # per sheet
    {"item_name": "Notepads",                         "category": "product",      "unit_price": 2.00},  # per pad
    {"item_name": "Invitation cards",                 "category": "product",      "unit_price": 0.50},  # per card
    {"item_name": "Flyers",                           "category": "product",      "unit_price": 0.15},  # per flyer
    {"item_name": "Party streamers",                  "category": "product",      "unit_price": 0.05},  # per roll
    {"item_name": "Decorative adhesive tape (washi tape)", "category": "product", "unit_price": 0.20},  # per roll
    {"item_name": "Paper party bags",                 "category": "product",      "unit_price": 0.25},  # per bag
    {"item_name": "Name tags with lanyards",          "category": "product",      "unit_price": 0.75},  # per tag
    {"item_name": "Presentation folders",             "category": "product",      "unit_price": 0.50},  # per folder

    # Large-format items (priced per unit)
    {"item_name": "Large poster paper (24x36 inches)", "category": "large_format", "unit_price": 1.00},
    {"item_name": "Rolls of banner paper (36-inch width)", "category": "large_format", "unit_price": 2.50},

    # Specialty papers
    {"item_name": "100 lb cover stock",               "category": "specialty",    "unit_price": 0.50},
    {"item_name": "80 lb text paper",                 "category": "specialty",    "unit_price": 0.40},
    {"item_name": "250 gsm cardstock",                "category": "specialty",    "unit_price": 0.30},
    {"item_name": "220 gsm poster paper",             "category": "specialty",    "unit_price": 0.35},
]

# Given below are some utility functions you can use to implement your multi-agent system

def generate_sample_inventory(paper_supplies: list, coverage: float = 0.4, seed: int = 137) -> pd.DataFrame:
    """
    Generate inventory for exactly a specified percentage of items from the full paper supply list.

    This function randomly selects exactly `coverage` × N items from the `paper_supplies` list,
    and assigns each selected item:
    - a random stock quantity between 200 and 800,
    - a minimum stock level between 50 and 150.

    The random seed ensures reproducibility of selection and stock levels.

    Args:
        paper_supplies (list): A list of dictionaries, each representing a paper item with
                               keys 'item_name', 'category', and 'unit_price'.
        coverage (float, optional): Fraction of items to include in the inventory (default is 0.4, or 40%).
        seed (int, optional): Random seed for reproducibility (default is 137).

    Returns:
        pd.DataFrame: A DataFrame with the selected items and assigned inventory values, including:
                      - item_name
                      - category
                      - unit_price
                      - current_stock
                      - min_stock_level
    """
    # Ensure reproducible random output
    np.random.seed(seed)

    # Calculate number of items to include based on coverage
    num_items = int(len(paper_supplies) * coverage)

    # Randomly select item indices without replacement
    selected_indices = np.random.choice(
        range(len(paper_supplies)),
        size=num_items,
        replace=False
    )

    # Extract selected items from paper_supplies list
    selected_items = [paper_supplies[i] for i in selected_indices]

    # Construct inventory records
    inventory = []
    for item in selected_items:
        inventory.append({
            "item_name": item["item_name"],
            "category": item["category"],
            "unit_price": item["unit_price"],
            "current_stock": np.random.randint(200, 800),  # Realistic stock range
            "min_stock_level": np.random.randint(50, 150)  # Reasonable threshold for reordering
        })

    # Return inventory as a pandas DataFrame
    return pd.DataFrame(inventory)

def init_database(db_engine: Engine, seed: int = 137) -> Engine:    
    """
    Set up the Munder Difflin database with all required tables and initial records.

    This function performs the following tasks:
    - Creates the 'transactions' table for logging stock orders and sales
    - Loads customer inquiries from 'quote_requests.csv' into a 'quote_requests' table
    - Loads previous quotes from 'quotes.csv' into a 'quotes' table, extracting useful metadata
    - Generates a random subset of paper inventory using `generate_sample_inventory`
    - Inserts initial financial records including available cash and starting stock levels

    Args:
        db_engine (Engine): A SQLAlchemy engine connected to the SQLite database.
        seed (int, optional): A random seed used to control reproducibility of inventory stock levels.
                              Default is 137.

    Returns:
        Engine: The same SQLAlchemy engine, after initializing all necessary tables and records.

    Raises:
        Exception: If an error occurs during setup, the exception is printed and raised.
    """
    try:
        # ----------------------------
        # 1. Create an empty 'transactions' table schema
        # ----------------------------
        transactions_schema = pd.DataFrame({
            "id": [],
            "item_name": [],
            "transaction_type": [],  # 'stock_orders' or 'sales'
            "units": [],             # Quantity involved
            "price": [],             # Total price for the transaction
            "transaction_date": [],  # ISO-formatted date
        })
        transactions_schema.to_sql("transactions", db_engine, if_exists="replace", index=False)

        # Set a consistent starting date
        initial_date = datetime(2025, 1, 1).isoformat()

        # ----------------------------
        # 2. Load and initialize 'quote_requests' table
        # ----------------------------
        quote_requests_df = pd.read_csv("quote_requests.csv")
        quote_requests_df["id"] = range(1, len(quote_requests_df) + 1)
        quote_requests_df.to_sql("quote_requests", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 3. Load and transform 'quotes' table
        # ----------------------------
        quotes_df = pd.read_csv("quotes.csv")
        quotes_df["request_id"] = range(1, len(quotes_df) + 1)
        quotes_df["order_date"] = initial_date

        # Unpack metadata fields (job_type, order_size, event_type) if present
        if "request_metadata" in quotes_df.columns:
            quotes_df["request_metadata"] = quotes_df["request_metadata"].apply(
                lambda x: ast.literal_eval(x) if isinstance(x, str) else x
            )
            quotes_df["job_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("job_type", ""))
            quotes_df["order_size"] = quotes_df["request_metadata"].apply(lambda x: x.get("order_size", ""))
            quotes_df["event_type"] = quotes_df["request_metadata"].apply(lambda x: x.get("event_type", ""))

        # Retain only relevant columns
        quotes_df = quotes_df[[
            "request_id",
            "total_amount",
            "quote_explanation",
            "order_date",
            "job_type",
            "order_size",
            "event_type"
        ]]
        quotes_df.to_sql("quotes", db_engine, if_exists="replace", index=False)

        # ----------------------------
        # 4. Generate inventory and seed stock
        # ----------------------------
        inventory_df = generate_sample_inventory(paper_supplies, seed=seed)

        # Seed initial transactions
        initial_transactions = []

        # Add a starting cash balance via a dummy sales transaction
        initial_transactions.append({
            "item_name": None,
            "transaction_type": "sales",
            "units": None,
            "price": 50000.0,
            "transaction_date": initial_date,
        })

        # Add one stock order transaction per inventory item
        for _, item in inventory_df.iterrows():
            initial_transactions.append({
                "item_name": item["item_name"],
                "transaction_type": "stock_orders",
                "units": item["current_stock"],
                "price": item["current_stock"] * item["unit_price"],
                "transaction_date": initial_date,
            })

        # Commit transactions to database
        pd.DataFrame(initial_transactions).to_sql("transactions", db_engine, if_exists="append", index=False)

        # Save the inventory reference table
        inventory_df.to_sql("inventory", db_engine, if_exists="replace", index=False)

        return db_engine

    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def create_transaction(
    item_name: str,
    transaction_type: str,
    quantity: int,
    price: float,
    date: Union[str, datetime],
) -> int:
    """
    This function records a transaction of type 'stock_orders' or 'sales' with a specified
    item name, quantity, total price, and transaction date into the 'transactions' table of the database.

    Args:
        item_name (str): The name of the item involved in the transaction.
        transaction_type (str): Either 'stock_orders' or 'sales'.
        quantity (int): Number of units involved in the transaction.
        price (float): Total price of the transaction.
        date (str or datetime): Date of the transaction in ISO 8601 format.

    Returns:
        int: The ID of the newly inserted transaction.

    Raises:
        ValueError: If `transaction_type` is not 'stock_orders' or 'sales'.
        Exception: For other database or execution errors.
    """
    try:
        # Convert datetime to ISO string if necessary
        date_str = date.isoformat() if isinstance(date, datetime) else date

        # Validate transaction type
        if transaction_type not in {"stock_orders", "sales"}:
            raise ValueError("Transaction type must be 'stock_orders' or 'sales'")

        # Prepare transaction record as a single-row DataFrame
        transaction = pd.DataFrame([{
            "item_name": item_name,
            "transaction_type": transaction_type,
            "units": quantity,
            "price": price,
            "transaction_date": date_str,
        }])

        # Insert the record into the database
        transaction.to_sql("transactions", db_engine, if_exists="append", index=False)

        # Fetch and return the ID of the inserted row
        result = pd.read_sql("SELECT last_insert_rowid() as id", db_engine)
        return int(result.iloc[0]["id"])

    except Exception as e:
        print(f"Error creating transaction: {e}")
        raise

def get_all_inventory(as_of_date: str) -> Dict[str, int]:
    """
    Retrieve a snapshot of available inventory as of a specific date.

    This function calculates the net quantity of each item by summing 
    all stock orders and subtracting all sales up to and including the given date.

    Only items with positive stock are included in the result.

    Args:
        as_of_date (str): ISO-formatted date string (YYYY-MM-DD) representing the inventory cutoff.

    Returns:
        Dict[str, int]: A dictionary mapping item names to their current stock levels.
    """
    # SQL query to compute stock levels per item as of the given date
    query = """
        SELECT
            item_name,
            SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END) as stock
        FROM transactions
        WHERE item_name IS NOT NULL
        AND transaction_date <= :as_of_date
        GROUP BY item_name
        HAVING stock > 0
    """

    # Execute the query with the date parameter
    result = pd.read_sql(query, db_engine, params={"as_of_date": as_of_date})

    # Convert the result into a dictionary {item_name: stock}
    return dict(zip(result["item_name"], result["stock"]))

def get_stock_level(item_name: str, as_of_date: Union[str, datetime]) -> pd.DataFrame:
    """
    Retrieve the stock level of a specific item as of a given date.

    This function calculates the net stock by summing all 'stock_orders' and 
    subtracting all 'sales' transactions for the specified item up to the given date.

    Args:
        item_name (str): The name of the item to look up.
        as_of_date (str or datetime): The cutoff date (inclusive) for calculating stock.

    Returns:
        pd.DataFrame: A single-row DataFrame with columns 'item_name' and 'current_stock'.
    """
    # Convert date to ISO string format if it's a datetime object
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # SQL query to compute net stock level for the item
    stock_query = """
        SELECT
            item_name,
            COALESCE(SUM(CASE
                WHEN transaction_type = 'stock_orders' THEN units
                WHEN transaction_type = 'sales' THEN -units
                ELSE 0
            END), 0) AS current_stock
        FROM transactions
        WHERE item_name = :item_name
        AND transaction_date <= :as_of_date
    """

    # Execute query and return result as a DataFrame
    return pd.read_sql(
        stock_query,
        db_engine,
        params={"item_name": item_name, "as_of_date": as_of_date},
    )

def get_supplier_delivery_date(input_date_str: str, quantity: int) -> str:
    """
    Estimate the supplier delivery date based on the requested order quantity and a starting date.

    Delivery lead time increases with order size:
        - ≤10 units: same day
        - 11–100 units: 1 day
        - 101–1000 units: 4 days
        - >1000 units: 7 days

    Args:
        input_date_str (str): The starting date in ISO format (YYYY-MM-DD).
        quantity (int): The number of units in the order.

    Returns:
        str: Estimated delivery date in ISO format (YYYY-MM-DD).
    """
    # Debug log (comment out in production if needed)
    print(f"FUNC (get_supplier_delivery_date): Calculating for qty {quantity} from date string '{input_date_str}'")

    # Attempt to parse the input date
    try:
        input_date_dt = datetime.fromisoformat(input_date_str.split("T")[0])
    except (ValueError, TypeError):
        # Fallback to current date on format error
        print(f"WARN (get_supplier_delivery_date): Invalid date format '{input_date_str}', using today as base.")
        input_date_dt = datetime.now()

    # Determine delivery delay based on quantity
    if quantity <= 10:
        days = 0
    elif quantity <= 100:
        days = 1
    elif quantity <= 1000:
        days = 4
    else:
        days = 7

    # Add delivery days to the starting date
    delivery_date_dt = input_date_dt + timedelta(days=days)

    # Return formatted delivery date
    return delivery_date_dt.strftime("%Y-%m-%d")

def get_cash_balance(as_of_date: Union[str, datetime]) -> float:
    """
    Calculate the current cash balance as of a specified date.

    The balance is computed by subtracting total stock purchase costs ('stock_orders')
    from total revenue ('sales') recorded in the transactions table up to the given date.

    Args:
        as_of_date (str or datetime): The cutoff date (inclusive) in ISO format or as a datetime object.

    Returns:
        float: Net cash balance as of the given date. Returns 0.0 if no transactions exist or an error occurs.
    """
    try:
        # Convert date to ISO format if it's a datetime object
        if isinstance(as_of_date, datetime):
            as_of_date = as_of_date.isoformat()

        # Query all transactions on or before the specified date
        transactions = pd.read_sql(
            "SELECT * FROM transactions WHERE transaction_date <= :as_of_date",
            db_engine,
            params={"as_of_date": as_of_date},
        )

        # Compute the difference between sales and stock purchases
        if not transactions.empty:
            total_sales = transactions.loc[transactions["transaction_type"] == "sales", "price"].sum()
            total_purchases = transactions.loc[transactions["transaction_type"] == "stock_orders", "price"].sum()
            return float(total_sales - total_purchases)

        return 0.0

    except Exception as e:
        print(f"Error getting cash balance: {e}")
        return 0.0


def generate_financial_report(as_of_date: Union[str, datetime]) -> Dict:
    """
    Generate a complete financial report for the company as of a specific date.

    This includes:
    - Cash balance
    - Inventory valuation
    - Combined asset total
    - Itemized inventory breakdown
    - Top 5 best-selling products

    Args:
        as_of_date (str or datetime): The date (inclusive) for which to generate the report.

    Returns:
        Dict: A dictionary containing the financial report fields:
            - 'as_of_date': The date of the report
            - 'cash_balance': Total cash available
            - 'inventory_value': Total value of inventory
            - 'total_assets': Combined cash and inventory value
            - 'inventory_summary': List of items with stock and valuation details
            - 'top_selling_products': List of top 5 products by revenue
    """
    # Normalize date input
    if isinstance(as_of_date, datetime):
        as_of_date = as_of_date.isoformat()

    # Get current cash balance
    cash = get_cash_balance(as_of_date)

    # Get current inventory snapshot
    inventory_df = pd.read_sql("SELECT * FROM inventory", db_engine)
    inventory_value = 0.0
    inventory_summary = []

    # Compute total inventory value and summary by item
    for _, item in inventory_df.iterrows():
        stock_info = get_stock_level(item["item_name"], as_of_date)
        stock = stock_info["current_stock"].iloc[0]
        item_value = stock * item["unit_price"]
        inventory_value += item_value

        inventory_summary.append({
            "item_name": item["item_name"],
            "stock": stock,
            "unit_price": item["unit_price"],
            "value": item_value,
        })

    # Identify top-selling products by revenue
    top_sales_query = """
        SELECT item_name, SUM(units) as total_units, SUM(price) as total_revenue
        FROM transactions
        WHERE transaction_type = 'sales' AND transaction_date <= :date
        GROUP BY item_name
        ORDER BY total_revenue DESC
        LIMIT 5
    """
    top_sales = pd.read_sql(top_sales_query, db_engine, params={"date": as_of_date})
    top_selling_products = top_sales.to_dict(orient="records")

    return {
        "as_of_date": as_of_date,
        "cash_balance": cash,
        "inventory_value": inventory_value,
        "total_assets": cash + inventory_value,
        "inventory_summary": inventory_summary,
        "top_selling_products": top_selling_products,
    }


def search_quote_history(search_terms: List[str], limit: int = 5) -> List[Dict]:
    """
    Retrieve a list of historical quotes that match any of the provided search terms.

    The function searches both the original customer request (from `quote_requests`) and
    the explanation for the quote (from `quotes`) for each keyword. Results are sorted by
    most recent order date and limited by the `limit` parameter.

    Args:
        search_terms (List[str]): List of terms to match against customer requests and explanations.
        limit (int, optional): Maximum number of quote records to return. Default is 5.

    Returns:
        List[Dict]: A list of matching quotes, each represented as a dictionary with fields:
            - original_request
            - total_amount
            - quote_explanation
            - job_type
            - order_size
            - event_type
            - order_date
    """
    conditions = []
    params = {}

    # Build SQL WHERE clause using LIKE filters for each search term
    for i, term in enumerate(search_terms):
        param_name = f"term_{i}"
        conditions.append(
            f"(LOWER(qr.response) LIKE :{param_name} OR "
            f"LOWER(q.quote_explanation) LIKE :{param_name})"
        )
        params[param_name] = f"%{term.lower()}%"

    # Combine conditions; fallback to always-true if no terms provided
    where_clause = " AND ".join(conditions) if conditions else "1=1"

    # Final SQL query to join quotes with quote_requests
    query = f"""
        SELECT
            qr.response AS original_request,
            q.total_amount,
            q.quote_explanation,
            q.job_type,
            q.order_size,
            q.event_type,
            q.order_date
        FROM quotes q
        JOIN quote_requests qr ON q.request_id = qr.id
        WHERE {where_clause}
        ORDER BY q.order_date DESC
        LIMIT {limit}
    """

    # Execute parameterized query
    with db_engine.connect() as conn:
        result = conn.execute(text(query), params)
        return [dict(row) for row in result]

########################
########################
########################
# YOUR MULTI AGENT STARTS HERE
########################
########################
########################

# Set up and load your env parameters and instantiate your model.


"""Set up tools for your agents to use, these should be methods that combine the database functions above
 and apply criteria to them to ensure that the flow of the system is correct."""

###############################################
# MULTI-AGENT SYSTEM (Pydantic-AI)
###############################################

from pydantic_ai import Agent, Tool, RunContext
from typing import List, Dict, Optional
import json
import re


###############################################
# REQUEST PARSING UTILITIES
###############################################

# Manual keyword → canonical item mapping.
# This does NOT need to cover every possible phrase; it just needs to
# reasonably map common request phrases to inventory item names.
ITEM_KEYWORDS = [
    ("a4 glossy paper", "Glossy paper"),
    ("glossy paper", "Glossy paper"),
    ("a4 matte paper", "Matte paper"),
    ("matte paper", "Matte paper"),
    ("cardstock", "Cardstock"),
    ("heavy cardstock", "Cardstock"),
    ("colored paper", "Colored paper"),
    ("colourful paper", "Colored paper"),
    ("construction paper", "Construction paper"),
    ("wrapping paper", "Wrapping paper"),
    ("glitter paper", "Glitter paper"),
    ("decorative paper", "Decorative paper"),
    ("recycled paper", "Recycled paper"),
    ("eco-friendly paper", "Eco-friendly paper"),

    ("a4 printer paper", "A4 paper"),
    ("a4 printing paper", "A4 paper"),
    ("a4 white paper", "A4 paper"),
    ("a4 paper", "A4 paper"),
    ("standard copy paper", "Standard copy paper"),
    ("copy paper", "Standard copy paper"),
    ("printer paper", "Standard copy paper"),
    ("printing paper", "Standard copy paper"),

    ("poster paper", "Poster paper"),
    ("large poster paper", "Large poster paper (24x36 inches)"),
    ("banner paper", "Banner paper"),
    ("banner rolls", "Rolls of banner paper (36-inch width)"),

    ("100 lb cover stock", "100 lb cover stock"),
    ("80 lb text paper", "80 lb text paper"),
    ("250 gsm cardstock", "250 gsm cardstock"),
    ("220 gsm poster paper", "220 gsm poster paper"),

    ("paper plates", "Paper plates"),
    ("plates", "Paper plates"),
    ("paper cups", "Paper cups"),
    ("cups", "Paper cups"),
    ("paper napkins", "Paper napkins"),
    ("napkins", "Paper napkins"),
    ("table covers", "Table covers"),

    ("envelopes", "Envelopes"),
    ("sticky notes", "Sticky notes"),
    ("notepads", "Notepads"),
    ("invitation cards", "Invitation cards"),
    ("flyers", "Flyers"),
    ("party streamers", "Party streamers"),
    ("streamers", "Party streamers"),
    ("washi tape", "Decorative adhesive tape (washi tape)"),
    ("decorative adhesive tape", "Decorative adhesive tape (washi tape)"),
    ("paper party bags", "Paper party bags"),
    ("name tags", "Name tags with lanyards"),
    ("folders", "Presentation folders"),
]


def _parse_due_date(request_text: str) -> Optional[str]:
    """
    Extract a 'needed by' date like 'April 15, 2025' from the request text.
    Returns ISO date string YYYY-MM-DD or None.
    """
    pattern = r"(?:by|before|no later than)\s+([A-Za-z]+ \d{1,2}, \d{4})"
    m = re.search(pattern, request_text)
    if not m:
        return None
    date_str = m.group(1)
    try:
        dt = datetime.strptime(date_str, "%B %d, %Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None


def _find_quantity_near(text_lower: str, keyword: str, start_idx: int) -> int:
    """
    Look backwards from keyword position for the nearest integer quantity.
    If 'reams' is mentioned near the number, treat each ream as 500 units.
    """
    window_start = max(0, start_idx - 60)
    window = text_lower[window_start:start_idx]

    # Find all integers in the window and take the last one
    nums = re.findall(r"(\d{1,6})", window)
    if not nums:
        return 0
    quantity = int(nums[-1])

    # If 'ream' appears near that number, convert to sheets (approx).
    ream_window = window + text_lower[start_idx:start_idx + len(keyword) + 20]
    if "ream" in ream_window:
        quantity *= 500

    return quantity


def parse_request_to_order(
    job: str,
    need_size: str,
    event: str,
    request_text: str,
    request_date: str,
) -> Dict:
    """
    Parse a raw customer request into a structured order dict.

    Returns a dict like:
    {
        "job": str,
        "order_size": str,
        "event_type": str,
        "request_date": "YYYY-MM-DD",
        "due_date": "YYYY-MM-DD" or None,
        "items": [
            {
                "item_name": str,
                "quantity": int,
                "raw_keyword": str
            },
            ...
        ],
        "unknown_items": [str, ...]
    }
    """
    text_lower = request_text.lower()
    due_date = _parse_due_date(request_text)

    items: List[Dict] = []
    seen_items = set()
    unknown_items: List[str] = []

    # Basic keyword-based mapping to known inventory items
    for keyword, canonical in ITEM_KEYWORDS:
        idx = text_lower.find(keyword)
        if idx == -1:
            continue

        qty = _find_quantity_near(text_lower, keyword, idx)
        if qty <= 0:
            # If we don't find a number, we still record that this item was mentioned.
            qty = 0

        if canonical in seen_items:
            # If same item appears multiple times, sum quantities
            for it in items:
                if it["item_name"] == canonical:
                    it["quantity"] += qty
                    break
        else:
            items.append(
                {
                    "item_name": canonical,
                    "quantity": qty,
                    "raw_keyword": keyword,
                }
            )
            seen_items.add(canonical)

    # Very simple unknown item detection for things we don't sell explicitly
    # (example: balloons, tickets).
    for maybe_unknown in ["balloons", "tickets"]:
        if maybe_unknown in text_lower:
            unknown_items.append(maybe_unknown)

    return {
        "job": job,
        "order_size": need_size,
        "event_type": event,
        "request_date": request_date,
        "due_date": due_date,
        "items": items,
        "unknown_items": list(set(unknown_items)),
        "raw_request": request_text,
    }

###############################################
# LOW-LEVEL "TOOLS" WRAPPING DB HELPERS
###############################################

def tool_get_stock_level(item_name: str, as_of_date: str) -> Dict:
    """Tool wrapper around get_stock_level."""
    df = get_stock_level(item_name, as_of_date)
    return df.to_dict(orient="records")[0]


def tool_get_all_inventory(as_of_date: str) -> Dict[str, int]:
    """Tool wrapper around get_all_inventory."""
    return get_all_inventory(as_of_date)


def tool_get_supplier_eta(start_date: str, quantity: int) -> str:
    """Tool wrapper around get_supplier_delivery_date."""
    return get_supplier_delivery_date(start_date, quantity)


def tool_get_cash_balance(as_of_date: str) -> float:
    """Tool wrapper around get_cash_balance."""
    return get_cash_balance(as_of_date)


def tool_create_stock_order(item_name: str, quantity: int, unit_price: float, order_date: str) -> Dict:
    """Tool wrapper around create_transaction for stock_orders."""
    total_price = quantity * unit_price
    tx_id = create_transaction(
        item_name=item_name,
        transaction_type="stock_orders",
        quantity=quantity,
        price=total_price,
        date=order_date,
    )
    return {"transaction_id": tx_id, "total_price": total_price}


def tool_create_sale(item_name: str, quantity: int, unit_price: float, sale_date: str) -> Dict:
    """Tool wrapper around create_transaction for sales."""
    total_price = quantity * unit_price
    tx_id = create_transaction(
        item_name=item_name,
        transaction_type="sales",
        quantity=quantity,
        price=total_price,
        date=sale_date,
    )
    return {"transaction_id": tx_id, "total_price": total_price}


def tool_generate_financial_report(as_of_date: str) -> Dict:
    """Tool wrapper around generate_financial_report."""
    return generate_financial_report(as_of_date)


def tool_search_quote_history(terms: List[str], limit: int = 5) -> List[Dict]:
    """Tool wrapper around search_quote_history."""
    return search_quote_history(terms, limit=limit)


def get_unit_price_for_item(item_name: str) -> float:
    """
    Helper to get the unit_price for an item.

    Tries the inventory table first; if not found, falls back to the
    paper_supplies list defined at the top of the file.
    """
    try:
        df = pd.read_sql(
            "SELECT unit_price FROM inventory WHERE item_name = :name LIMIT 1",
            db_engine,
            params={"name": item_name},
        )
        if not df.empty:
            return float(df["unit_price"].iloc[0])
    except Exception:
        pass

    # Fallback to static list
    for it in paper_supplies:
        if it["item_name"].lower() == item_name.lower():
            return it["unit_price"]

    # Last resort default
    return 0.10


###############################################
# INVENTORY AGENT LOGIC
###############################################

def inventory_agent_handle(parsed_order: Dict) -> Dict:
    """
    Inventory 'agent'.

    Input: parsed_order dict from parse_request_to_order.
    Output: inventory assessment dict:

    {
      "stock_ok": bool,
      "item_status": {
         item_name: { "requested": int, "available": int, "need_to_reorder": int }
      },
      "reorder_list": [
         { "item_name": str, "quantity": int, "unit_price": float }
      ],
      "delivery_date": "YYYY-MM-DD"
    }
    """
    request_date = parsed_order["request_date"]
    due_date = parsed_order.get("due_date") or request_date

    item_status: Dict[str, Dict] = {}
    reorder_list: List[Dict] = []
    stock_ok = True
    total_reorder_qty = 0

    for item in parsed_order["items"]:
        name = item["item_name"]
        requested = int(item.get("quantity") or 0)

        # Get current stock
        stock_info = tool_get_stock_level(name, request_date)
        available = int(stock_info.get("current_stock", 0))

        need_to_reorder = max(0, requested - available)

        unit_price = get_unit_price_for_item(name)

        item_status[name] = {
            "requested": requested,
            "available": available,
            "need_to_reorder": need_to_reorder,
            "unit_price": unit_price,
        }

        if need_to_reorder > 0:
            stock_ok = False
            total_reorder_qty += need_to_reorder
            reorder_list.append(
                {"item_name": name, "quantity": need_to_reorder, "unit_price": unit_price}
            )

    # Estimate delivery date:
    if total_reorder_qty > 0:
        eta = tool_get_supplier_eta(request_date, total_reorder_qty)
        delivery_date = eta
    else:
        # If everything is in stock, assume we can ship on the request date.
        delivery_date = request_date

    # Choose the earlier of due_date and eta? For simplicity, keep eta,
    # but in text we can mention if we comfortably meet due_date.
    return {
        "stock_ok": stock_ok,
        "item_status": item_status,
        "reorder_list": reorder_list,
        "delivery_date": delivery_date,
        "due_date_requested": due_date,
    }


###############################################
# QUOTING AGENT LOGIC
###############################################

def quoting_agent_handle(parsed_order: Dict) -> Dict:
    """
    Quoting 'agent'.

    Uses:
      - get_unit_price_for_item
      - tool_search_quote_history
      - tool_get_cash_balance

    Returns:
    {
      "total": float,
      "items": { item_name: { "qty": int, "unit_price": float, "subtotal": float } },
      "discount": float,
      "explanation": str
    }
    """
    request_date = parsed_order["request_date"]
    job = parsed_order["job"]
    order_size = parsed_order["order_size"]
    event_type = parsed_order["event_type"]

    items_pricing: Dict[str, Dict] = {}
    gross_total = 0.0

    # Base prices and subtotals
    for item in parsed_order["items"]:
        name = item["item_name"]
        qty = int(item.get("quantity") or 0)
        if qty <= 0:
            continue

        unit_price = get_unit_price_for_item(name)
        subtotal = unit_price * qty
        gross_total += subtotal

        items_pricing[name] = {
            "qty": qty,
            "unit_price": unit_price,
            "subtotal": subtotal,
        }

    # Look up similar past quotes (we mainly use this as justification text)
    terms = [t for t in [job, order_size, event_type] if t]
    history = tool_search_quote_history(terms) if terms else []

    # Use cash balance to modulate how generous we are
    cash_balance = tool_get_cash_balance(request_date)

    # Base discount by order size
    if order_size == "large":
        base_discount_rate = 0.15
    elif order_size == "medium":
        base_discount_rate = 0.10
    else:
        base_discount_rate = 0.05

    # Adjust discount if cash is tight
    if cash_balance < 20000:
        base_discount_rate *= 0.7  # be less generous if low on cash

    discount = gross_total * base_discount_rate
    intermediate_total = gross_total - discount

    # Round to a "nice" number (nearest whole dollar)
    final_total = round(intermediate_total)

    explanation_parts = []
    explanation_parts.append(
        f"For your {order_size} order as a {job} organizing a {event_type}, "
        f"we calculated item costs based on our current unit prices and then applied "
        f"a bulk discount of about {int(base_discount_rate * 100)}%."
    )

    if history:
        explanation_parts.append(
            "We also checked several similar past quotes to ensure your pricing is consistent "
            "and competitive for this type of event."
        )

    if cash_balance < 20000:
        explanation_parts.append(
            "Because our current cash balance is a bit lower than usual, "
            "we applied a slightly more conservative discount while still keeping your total attractive."
        )
    else:
        explanation_parts.append(
            "Our healthy cash position allows us to offer a more generous discount on this order."
        )

    explanation_parts.append(
        f"The gross total before discount was approximately ${gross_total:.2f}. "
        f"After discount and rounding to a simple, customer-friendly figure, "
        f"your final total comes to about ${final_total:.2f}."
    )

    explanation = " ".join(explanation_parts)

    return {
        "total": final_total,
        "items": items_pricing,
        "discount": gross_total - final_total,
        "explanation": explanation,
    }


###############################################
# ORDERING / TRANSACTIONS AGENT LOGIC
###############################################

def ordering_agent_handle(
    parsed_order: Dict,
    inventory_assessment: Dict,
    quote: Dict,
) -> Dict:
    """
    Ordering 'agent'.

    - Executes stock reorders (stock_orders transactions)
    - Records sales (sales transactions)

    Returns:
    {
      "sale_transactions": [ {...}, ... ],
      "reorder_transactions": [ {...}, ... ]
    }
    """
    date = parsed_order["request_date"]
    sale_transactions: List[Dict] = []
    reorder_transactions: List[Dict] = []

    # 1. Reorder if needed
    for r in inventory_assessment["reorder_list"]:
        tx = tool_create_stock_order(
            item_name=r["item_name"],
            quantity=r["quantity"],
            unit_price=r["unit_price"],
            order_date=date,
        )
        reorder_transactions.append(tx)

    # 2. Record sales for requested items
    #    (we assume we will fulfill the whole requested qty, given we reorder above)
    item_to_price = {name: info["unit_price"] for name, info in quote["items"].items()}

    for item in parsed_order["items"]:
        name = item["item_name"]
        qty = int(item.get("quantity") or 0)
        if qty <= 0:
            continue

        unit_price = item_to_price.get(name, get_unit_price_for_item(name))
        tx = tool_create_sale(
            item_name=name,
            quantity=qty,
            unit_price=unit_price,
            sale_date=date,
        )
        sale_transactions.append(tx)

    return {
        "sale_transactions": sale_transactions,
        "reorder_transactions": reorder_transactions,
    }

###############################################
# ORCHESTRATOR FUNCTION
###############################################

def call_multi_agent_system(
    job: str,
    need_size: str,
    event: str,
    request_text: str,
    request_date: str,
) -> str:
    """
    Main orchestration entry point used by run_test_scenarios().

    1. Parse the raw request text into a structured order.
    2. Call the inventory agent.
    3. Call the quoting agent.
    4. Call the ordering agent to create DB transactions.
    5. Return a customer-facing explanation string.
    """
    # 1. Parse
    parsed_order = parse_request_to_order(
        job=job,
        need_size=need_size,
        event=event,
        request_text=request_text,
        request_date=request_date,
    )

    # If no items were detected at all, respond gracefully
    if not parsed_order["items"]:
        return (
            "We were unable to map your request to our current catalog items. "
            "Please rephrase the items using standard paper product names."
        )

    # 2. Inventory assessment
    inventory_assessment = inventory_agent_handle(parsed_order)

    # 3. Quote
    quote = quoting_agent_handle(parsed_order)

    # 4. Ordering / transactions
    _tx_result = ordering_agent_handle(parsed_order, inventory_assessment, quote)

    # 5. Build customer-facing message
    delivery_date = inventory_assessment["delivery_date"]
    due_date = inventory_assessment["due_date_requested"]

    stock_note = ""
    if not inventory_assessment["stock_ok"]:
        stock_note = (
            "Some items require a supplier reorder; your delivery date reflects the extra lead time. "
        )
    else:
        stock_note = "All requested items are currently in stock. "

    due_note = ""
    if delivery_date <= due_date:
        due_note = (
            f"We can meet your requested deadline of {due_date} with an estimated delivery by {delivery_date}. "
        )
    else:
        due_note = (
            f"Due to supplier lead times, the earliest estimated delivery is {delivery_date}, "
            f"which is slightly later than your requested date of {due_date}. "
        )

    response = (
        f"Quote total: ${quote['total']:.2f}. "
        f"{stock_note}{due_note}{quote['explanation']}"
    )

    return response



###############################################
# TOOL DEFINITIONS
###############################################


# -------- Inventory Tools --------

@Tool
def get_stock_level_tool(item_name: str, as_of_date: str):
    """Return current stock level for one item."""
    df = get_stock_level(item_name, as_of_date)
    return df.to_dict(orient="records")[0]


@Tool
def get_all_inventory_tool(as_of_date: str):
    """Return snapshot of all inventory items."""
    inv = get_all_inventory(as_of_date)
    return inv


@Tool
def estimate_supplier_eta_tool(start_date: str, quantity: int):
    """Return estimated supplier delivery date for quantity."""
    return get_supplier_delivery_date(start_date, quantity)


@Tool
def cash_balance_tool(as_of_date: str):
    """Return cash balance as of a date."""
    return get_cash_balance(as_of_date)


@Tool
def reorder_stock_tool(item_name: str, quantity: int, unit_price: float, order_date: str):
    """
    Create a stock order transaction.
    Returns the transaction_id.
    """
    total_price = quantity * unit_price
    tid = create_transaction(
        item_name=item_name,
        transaction_type="stock_orders",
        quantity=quantity,
        price=total_price,
        date=order_date,
    )
    return {"transaction_id": tid, "total_price": total_price}


@Tool
def confirm_stock_tool(item_name: str, as_of_date: str):
    """Final stock check before fulfilling sale."""
    df = get_stock_level(item_name, as_of_date)
    return df.to_dict(orient="records")[0]["current_stock"]


# -------- Quoting Tools --------

@Tool
def search_quote_history_tool(terms: List[str]):
    """Return similar recent quotes."""
    return search_quote_history(terms)


@Tool
def q_cash_balance_tool(as_of_date: str):
    """Cash balance for discount adjustment."""
    return get_cash_balance(as_of_date)


# -------- Ordering / Transactions --------

@Tool
def record_sale_tool(item_name: str, quantity: int, unit_price: float, sale_date: str):
    """Record sale transaction."""
    total_price = quantity * unit_price
    tid = create_transaction(
        item_name=item_name,
        transaction_type="sales",
        quantity=quantity,
        price=total_price,
        date=sale_date,
    )
    return {"transaction_id": tid, "total_price": total_price}


@Tool
def reorder_if_needed_tool(item_name: str, quantity: int, unit_price: float, order_date: str):
    """Record an additional stock order if required."""
    total_price = quantity * unit_price
    tid = create_transaction(
        item_name=item_name,
        transaction_type="stock_orders",
        quantity=quantity,
        price=total_price,
        date=order_date,
    )
    return {"transaction_id": tid, "total_price": total_price}


@Tool
def financial_report_tool(as_of_date: str):
    """For internal diagnostics."""
    return generate_financial_report(as_of_date)



###############################################
# AGENT DEFINITIONS
###############################################

# Inventory Agent
inventory_agent = Agent(
    name="inventory_agent",
    instructions="""
    You are the Inventory Agent.
    Input: ParsedOrder JSON containing items with quantities.
    You must:
    - Check stock levels
    - Decide what needs reordering
    - Compute delivery feasibility dates
    - Return InventoryAssessment JSON:
        {
            "stock_ok": bool,
            "item_status": { item_name: {requested, available, need_to_reorder}},
            "reorder_list": [ {item_name, quantity, unit_price} ],
            "delivery_date": "YYYY-MM-DD"
        }
    """,
    tools=[
        get_stock_level_tool,
        get_all_inventory_tool,
        estimate_supplier_eta_tool,
        cash_balance_tool,
        reorder_stock_tool,
        confirm_stock_tool
    ]
)


# Quoting Agent
quoting_agent = Agent(
    name="quoting_agent",
    instructions="""
    You are the Quoting Agent.
    Input: ParsedOrder JSON containing items and metadata.
    Tasks:
    - Look up similar past quotes using search_quote_history_tool.
    - Determine pricing: item totals, discounts, round friendly.
    - Produce Quote JSON:
        {
            "total": float,
            "items": {item: {qty, unit_price, subtotal}},
            "discount": float,
            "explanation": str
        }
    """,
    tools=[
        search_quote_history_tool,
        q_cash_balance_tool
    ]
)


# Ordering Agent
ordering_agent = Agent(
    name="ordering_agent",
    instructions="""
    You are the Ordering & Transactions Agent.
    Input:
      - InventoryAssessment JSON
      - Quote JSON

    Responsibilities:
    - Execute reorder stock_orders if needed.
    - Record sale transactions.
    - Produce TransactionResult JSON:
        {
            "sale_transactions": [...],
            "reorder_transactions": [...]
        }
    """,
    tools=[
        record_sale_tool,
        reorder_if_needed_tool,
        financial_report_tool
    ]
)


# Orchestrator Agent
orchestrator = Agent(
    name="orchestrator",
    instructions="""
    You are the Orchestrator.

    Input: raw customer request string.

    Steps:
    1. Parse request (items, quantities, metadata, date).
    2. Send order info to Inventory Agent.
    3. Send same order info to Quoting Agent.
    4. Send InventoryAssessment + Quote to Ordering Agent.
    5. Return customer-facing response:
       - total
       - delivery date
       - explanation (no internal details)
    """,
)


###############################################
# ORCHESTRATION FUNCTION
###############################################

# I deleted async, it only accepts (request_text, request_date), so Python complains when I pass 5 arguments.

# Run your test scenarios by writing them here. Make sure to keep track of them.

def run_test_scenarios():
    print("Initializing Database...")
    init_database(db_engine)

    try:
        quote_requests_sample = pd.read_csv("quote_requests_sample.csv")
        quote_requests_sample["request_date"] = pd.to_datetime(
            quote_requests_sample["request_date"], format="%m/%d/%y", errors="coerce"
        )
        quote_requests_sample.dropna(subset=["request_date"], inplace=True)
        quote_requests_sample = quote_requests_sample.sort_values("request_date")
    except Exception as e:
        print(f"FATAL: Error loading test data: {e}")
        return

    quote_requests_sample = pd.read_csv("quote_requests_sample.csv")

    # Sort by date
    quote_requests_sample["request_date"] = pd.to_datetime(
        quote_requests_sample["request_date"]
    )
    quote_requests_sample = quote_requests_sample.sort_values("request_date")

    # Get initial state
    initial_date = quote_requests_sample["request_date"].min().strftime("%Y-%m-%d")
    report = generate_financial_report(initial_date)
    current_cash = report["cash_balance"]
    current_inventory = report["inventory_value"]

    ############
    ############
    ############
    # INITIALIZE YOUR MULTI AGENT SYSTEM HERE
    ############
    ############
    ############

    results = []
    for idx, row in quote_requests_sample.iterrows():
        request_date = row["request_date"].strftime("%Y-%m-%d")

        print(f"\n=== Request {idx+1} ===")
        print(f"Context: {row['job']} organizing {row['event']}")
        print(f"Request Date: {request_date}")
        print(f"Cash Balance: ${current_cash:.2f}")
        print(f"Inventory Value: ${current_inventory:.2f}")

        # Process request
        request_with_date = f"{row['request']} (Date of request: {request_date})"

        response = call_multi_agent_system(
            row["job"],
            row["need_size"],
            row["event"],
            request_with_date,
            request_date,
        )

        # Update state
        report = generate_financial_report(request_date)
        current_cash = report["cash_balance"]
        current_inventory = report["inventory_value"]

        print(f"Response: {response}")
        print(f"Updated Cash: ${current_cash:.2f}")
        print(f"Updated Inventory: ${current_inventory:.2f}")

        results.append(
            {
                "request_id": idx + 1,
                "request_date": request_date,
                "cash_balance": current_cash,
                "inventory_value": current_inventory,
                "response": response,
            }
        )

        time.sleep(1)

    # Final report
    final_date = quote_requests_sample["request_date"].max().strftime("%Y-%m-%d")
    final_report = generate_financial_report(final_date)
    print("\n===== FINAL FINANCIAL REPORT =====")
    print(f"Final Cash: ${final_report['cash_balance']:.2f}")
    print(f"Final Inventory: ${final_report['inventory_value']:.2f}")

    # Save results
    pd.DataFrame(results).to_csv("test_results.csv", index=False)
    return results


if __name__ == "__main__":
    results = run_test_scenarios()