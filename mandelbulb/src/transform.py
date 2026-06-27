import pandas as pd
import numpy as np


def transform_data(sales_df, products_df, stores_df):

    print("\n===== DATA TRANSFORMATION =====")

    # Merge sales + products
    merged_df = pd.merge(
        sales_df,
        products_df,
        on="product_id",
        how="left"
    )

    # Merge with stores
    merged_df = pd.merge(
        merged_df,
        stores_df,
        on="store_id",
        how="left"
    )

    print("\n===== MERGED DATA =====")
    print(merged_df.head())

    # Create total_revenue
    merged_df["total_revenue"] = (
        merged_df["quantity"] *
        merged_df["price"]
    )

    print("\n===== REVENUE STATISTICS =====")

    print(
        f"Mean Revenue: {np.mean(merged_df['total_revenue'])}"
    )

    print(
        f"Max Revenue: {np.max(merged_df['total_revenue'])}"
    )

    print(
        f"Min Revenue: {np.min(merged_df['total_revenue'])}"
    )

    city_revenue = (
        merged_df
        .groupby("city")["total_revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n===== TOTAL REVENUE BY CITY =====")
    print(city_revenue)

    return merged_df, city_revenue