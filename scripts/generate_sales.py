import pandas as pd
from datetime import datetime
import random

data = []

for i in range(100):
    data.append({
        "order_id": i,
        "store_id": random.randint(1, 5),
        "product_id": random.randint(1, 20),
        "qty": random.randint(1, 5),
        "price": round(random.uniform(10, 500), 2),
        "date": datetime.today().strftime('%Y-%m-%d')
    })

df = pd.DataFrame(data)

df.to_csv("D:/Data Engineering/Practice/Projects/retailpulse\datasets/sales_2026-05-02.csv", index=False)

print("CSV generated")