
from pathlib import Path

import pandas as pd


# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

ORDERS_FILE = RAW_DATA_DIR / "orders.csv"


# Required Shopify order columns
REQUIRED_ORDER_COLUMNS = [
    "Order ID",
    "Order name",
    "Day",
    "Product title",
    "Product variant SKU",
    "Quantity ordered",
    "Gross sales",
    "Discounts",
    "Net sales",
]


def load_orders(file_path: Path = ORDERS_FILE) -> pd.DataFrame:
    """
    Load and clean Shopify order-level line-item data.

    Each row represents a product line or an order adjustment.
    Multiple rows can belong to the same order.
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"Orders CSV not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    # Remove accidental whitespace from column names
    df.columns = df.columns.str.strip()

    # Validate required columns
    missing_columns = [
        column
        for column in REQUIRED_ORDER_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Clean text columns without removing missing values
    text_columns = [
        "Order ID",
        "Order name",
        "Product title",
        "Product variant SKU",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # Parse order date
    df["Day"] = pd.to_datetime(
        df["Day"],
        errors="coerce"
    )

    # Convert numeric columns safely
    numeric_columns = [
        "Quantity ordered",
        "Gross sales",
        "Discounts",
        "Net sales",
    ]

    for column in numeric_columns:
        cleaned = (
            df[column]
            .astype("string")
            .str.replace(r"[$,]", "", regex=True)
            .str.strip()
        )

        df[column] = pd.to_numeric(
            cleaned,
            errors="coerce"
        )

    return df


def get_orders_data_quality(df: pd.DataFrame) -> dict:
    """
    Return a basic data-quality report.
    """

    return {
        "total_rows": len(df),
        "unique_orders": df["Order ID"].nunique(),
        "missing_order_ids": int(
            df["Order ID"].isna().sum()
        ),
        "missing_product_names": int(
            df["Product title"].isna().sum()
        ),
        "invalid_dates": int(
            df["Day"].isna().sum()
        ),
        "missing_net_sales": int(
            df["Net sales"].isna().sum()
        ),
        "duplicate_rows": int(
            df.duplicated().sum()
        ),
    }


if __name__ == "__main__":
    orders = load_orders()

    print("\nORDERS DATA LOADED SUCCESSFULLY")
    print("-" * 40)

    print(get_orders_data_quality(orders))

    print("\nSample records:")
    print(
        orders[
            ["Order ID", "Day", "Product title", "Net sales"]
        ].head()
    )
