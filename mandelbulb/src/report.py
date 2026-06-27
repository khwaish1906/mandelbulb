def generate_summary_report(
    final_df,
    city_revenue,
    top_products
):

    print("\n===== SUMMARY REPORT =====")

    total_transactions = len(final_df)

    total_revenue = final_df["total_revenue"].sum()

    top_city = city_revenue.idxmax()

    top_product = top_products.iloc[0]["product_name"]

    print(f"Total Transactions : {total_transactions}")
    print(f"Total Revenue      : {total_revenue}")
    print(f"Top Selling City   : {top_city}")
    print(f"Top Selling Product: {top_product}")