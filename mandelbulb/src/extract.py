import pandas as pd


def load_data(sales_file, products_file, stores_file):
    """
    Load CSV files into DataFrames.
    """

    try:
        sales_df = pd.read_csv(sales_file)
        products_df = pd.read_csv(products_file)
        stores_df = pd.read_csv(stores_file)

        print("\n===== SALES DATA =====")
        print("Shape:", sales_df.shape)
        print(sales_df.head())

        print("\n===== PRODUCTS DATA =====")
        print("Shape:", products_df.shape)
        print(products_df.head())

        print("\n===== STORES DATA =====")
        print("Shape:", stores_df.shape)
        print(stores_df.head())

        return sales_df, products_df, stores_df

    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None, None, None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None, None