def check_missing_values(df, df_name):

    print(f"\n===== MISSING VALUE REPORT : {df_name} =====")

    missing = df.isnull().sum()

    print(missing)

    print("-" * 40)

    return missing