import pandas as pd


def clean_sales_data(sales_df):

    print("\n===== CLEANING SALES DATA =====")

    # Remove duplicate rows
    duplicates = sales_df.duplicated().sum()

    print(f"Duplicate rows found: {duplicates}")

    sales_df = sales_df.drop_duplicates()

    print(f"Duplicate rows removed: {duplicates}")

    # Fill missing quantity with 0
    sales_df["quantity"] = sales_df["quantity"].fillna(0)

    # Drop rows where amount is NULL
    sales_df = sales_df.dropna(subset=["amount"])

    # Convert data types
    sales_df["sale_date"] = pd.to_datetime(sales_df["sale_date"])

    sales_df["amount"] = sales_df["amount"].astype(float)

    print(f"Cleaned DataFrame Shape: {sales_df.shape}")

    return sales_df