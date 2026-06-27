from sqlalchemy import create_engine


def load_to_database(df, database_path):

    print("\n===== LOADING DATA TO SQLITE =====")

    engine = create_engine(
        f"sqlite:///{database_path}"
    )

    df.to_sql(
        "retail_sales",
        engine,
        if_exists="replace",
        index=False
    )

    print("Data loaded successfully into retail_sales table")