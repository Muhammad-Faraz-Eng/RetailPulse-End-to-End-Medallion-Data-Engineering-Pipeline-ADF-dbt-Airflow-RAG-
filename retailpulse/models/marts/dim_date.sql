with dates as (
    select distinct cast(date as DATE) as date
    from dbo.silver_sales
)

select 
    date as date_id,
    date as full_date,
    YEAR(date) as year,
    MONTH(date) as month,
    DAY(date) as date,
    DATENAME(WEEKDAY, date) as weekday
from
    dates