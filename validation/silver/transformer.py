import pandas as pd


def transform_sales(df: pd.DataFrame):
    df = df.copy()

    df["order_id"] = df["order_id"].astype(int)
    df["store_id"] = df["store_id"].astype(int)
    df["product_id"] = df["product_id"].astype(int)

    df["qty"] = df["qty"].astype(int)
    df["price"] = df["price"].astype(float)

    df["date"] = pd.to_datetime(df["date"])

    df["total_amount"] = df["qty"] * df["price"]

    df.drop_duplicates(inplace=True)

    return df


def transform_products(df: pd.DataFrame):
    df = df.copy()

    df = df[["id", "title", "price", "category"]]

    df["id"] = df["id"].astype(int)
    df["price"] = df["price"].astype(float)

    df.drop_duplicates(inplace=True)

    return df


def transform_currency(df: pd.DataFrame):
    df = df.copy()

    df.rename(columns={"currency_code": "currency"}, inplace=True)

    df["base_code"] = df["base_code"].astype(str)
    df["currency"] = df["currency"].astype(str)
    df["rate"] = df["rate"].astype(float)

    df.drop_duplicates(inplace=True)

    return df


TRANSFORMER_REGISTRY = {
    "transform_sales": transform_sales,
    "transform_products": transform_products,
    "transform_currency": transform_currency,
}
