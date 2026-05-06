select 
    store_id,
    YEAR(cast(date as date)) as year,
    MONTH(cast(date as date)) as month,
    SUM(total_amount) as revenue
from dbo.fact_sales
group by 
    store_id,
    YEAR(cast(date as date)),
    MONTH(cast(date as date))