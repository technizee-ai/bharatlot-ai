
import pandas as pd


def calculate_sales_overview(orders: pd.DataFrame) -> dict:
    """
    Calculate order-level and sales overview metrics.
    """

    valid_orders = orders.dropna(subset=["Order ID"])

    # Sum all line-item and adjustment amounts per order.
    order_totals = (
        valid_orders.groupby("Order ID")["Net sales"]
        .sum()
    )

    total_orders = len(order_totals)
    total_net_sales = float(order_totals.sum())

    average_order_value = (
        total_net_sales / total_orders
        if total_orders > 0 else 0
    )

    return {
        "total_orders": int(total_orders),
        "total_net_sales": round(total_net_sales, 2),
        "average_order_value": round(
            average_order_value, 2
        ),
        "total_units_sold": int(
            valid_orders["Quantity ordered"].fillna(0).sum()
        ),
        "total_discounts": round(
            float(valid_orders["Discounts"].fillna(0).sum()),
            2
        ),
        "total_gross_sales": round(
            float(valid_orders["Gross sales"].fillna(0).sum()),
            2
        ),
    }


def get_top_products(
    orders: pd.DataFrame,
    limit: int = 10
) -> pd.DataFrame:
    """
    Identify top products by net sales.

    Rows without product names are excluded from
    product-level analysis, but remain in order totals.
    """

    products = orders.dropna(subset=["Product title"]).copy()

    product_summary = (
        products.groupby("Product title")
        .agg(
            units_sold=("Quantity ordered", "sum"),
            net_sales=("Net sales", "sum"),
            order_count=("Order ID", "nunique"),
        )
        .reset_index()
    )

    return (
        product_summary
        .sort_values("net_sales", ascending=False)
        .head(limit)
        .reset_index(drop=True)
    )


def get_daily_sales_trend(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily net sales at order level.
    """

    valid_orders = orders.dropna(
        subset=["Order ID", "Day"]
    )

    daily_orders = (
        valid_orders.groupby(
            ["Day", "Order ID"], as_index=False
        )["Net sales"].sum()
    )

    daily_sales = (
        daily_orders.groupby("Day", as_index=False)
        .agg(
            net_sales=("Net sales", "sum"),
            order_count=("Order ID", "nunique"),
        )
        .sort_values("Day")
    )

    return daily_sales


if __name__ == "__main__":
    from analytics.data_loader import load_orders

    orders = load_orders()

    overview = calculate_sales_overview(orders)

    print("\nBHARATLOT SALES OVERVIEW")
    print("=" * 40)

    for metric, value in overview.items():
        print(f"{metric}: {value}")

    print("\nTOP 10 PRODUCTS")
    print("=" * 40)
    print(get_top_products(orders).to_string(index=False))

    print("\nDAILY SALES TREND")
    print("=" * 40)
    print(get_daily_sales_trend(orders).tail(10).to_string(index=False))
