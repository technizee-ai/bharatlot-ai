
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INVENTORY_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "current_inventory_2026-11-10.csv"
)

REQUIRED_COLUMNS = [
    "Product variant SKU",
    "Product title",
    "Product variant title",
    "Inventory is tracked",
    "Ending inventory units",
    "Ending inventory value",
    "Ending inventory retail value",
    "Inventory units sold",
    "Sell-through rate",
    "Days of inventory remaining",
]


def load_inventory(file_path: Path = INVENTORY_FILE) -> pd.DataFrame:
    """Load and validate Shopify inventory data."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Inventory file not found: {file_path}"
        )

    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()

    missing = [
        col for col in REQUIRED_COLUMNS
        if col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing inventory columns: {missing}"
        )

    # Clean text fields
    text_columns = [
        "Product variant SKU",
        "Product title",
        "Product variant title",
    ]

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()

    # Convert numeric fields safely
    numeric_columns = [
        "Ending inventory units",
        "Ending inventory value",
        "Ending inventory retail value",
        "Inventory units sold",
        "Sell-through rate",
        "Days of inventory remaining",
    ]

    for col in numeric_columns:
        cleaned = (
            df[col]
            .astype("string")
            .str.replace(r"[$,%]", "", regex=True)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(
            cleaned,
            errors="coerce"
        )

    return df


def calculate_inventory_overview(
    inventory: pd.DataFrame,
    low_stock_threshold: int = 5,
    excess_stock_days: int = 90,
) -> dict:
    """Calculate inventory KPIs."""

    tracked = inventory[
        inventory["Inventory is tracked"]
        .astype("string")
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1"])
    ].copy()

    units = tracked["Ending inventory units"]

    return {
        "total_variants": int(len(inventory)),
        "tracked_variants": int(len(tracked)),
        "total_stock_units": int(units.sum()),
        "out_of_stock_variants": int(
            (units == 0).sum()
        ),
        "low_stock_variants": int(
            ((units > 0) & (units <= low_stock_threshold)).sum()
        ),
        "excess_stock_variants": int(
            (
                (units > 0)
                & (
                    tracked["Days of inventory remaining"]
                    > excess_stock_days
                )
            ).sum()
        ),
        "total_inventory_cost": round(
            tracked["Ending inventory value"].sum(),
            2,
        ),
        "total_inventory_retail_value": round(
            tracked["Ending inventory retail value"].sum(),
            2,
        ),
    }


def get_low_stock_products(
    inventory: pd.DataFrame,
    threshold: int = 5,
) -> pd.DataFrame:
    """Identify tracked variants with low stock."""

    tracked = inventory[
        inventory["Inventory is tracked"]
        .astype("string")
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1"])
    ]

    low_stock = tracked[
        (tracked["Ending inventory units"] > 0)
        & (tracked["Ending inventory units"] <= threshold)
    ]

    columns = [
        "Product variant SKU",
        "Product title",
        "Product variant title",
        "Ending inventory units",
        "Days of inventory remaining",
    ]

    return (
        low_stock[columns]
        .sort_values(
            "Ending inventory units",
            ascending=True
        )
        .reset_index(drop=True)
    )


def get_excess_stock_products(
    inventory: pd.DataFrame,
    days_threshold: int = 90,
) -> pd.DataFrame:
    """Identify variants with high estimated stock coverage."""

    tracked = inventory[
        inventory["Inventory is tracked"]
        .astype("string")
        .str.strip()
        .str.lower()
        .isin(["true", "yes", "1"])
    ]

    excess = tracked[
        (tracked["Ending inventory units"] > 0)
        & (
            tracked["Days of inventory remaining"]
            > days_threshold
        )
    ]

    columns = [
        "Product variant SKU",
        "Product title",
        "Ending inventory units",
        "Days of inventory remaining",
        "Ending inventory value",
    ]

    return (
        excess[columns]
        .sort_values(
            "Days of inventory remaining",
            ascending=False
        )
        .reset_index(drop=True)
    )


if __name__ == "__main__":
    inventory = load_inventory()

    print("\nBHARATLOT INVENTORY OVERVIEW")
    print("=" * 45)

    overview = calculate_inventory_overview(inventory)

    for metric, value in overview.items():
        print(f"{metric}: {value}")

    print("\nLOW STOCK VARIANTS")
    print("=" * 45)
    print(get_low_stock_products(inventory).head(15).to_string(index=False))

    print("\nEXCESS STOCK VARIANTS")
    print("=" * 45)
    print(get_excess_stock_products(inventory).head(15).to_string(index=False))
