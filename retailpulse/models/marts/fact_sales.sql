select 
    s.order_id as sale_id,
    s.product_id,
    s.store_id,
    CAST(s.date as DATE) as date,
    s.qty,
    s.price,
    s.total_amount
from    
     {{ ref('stg_sales') }} s