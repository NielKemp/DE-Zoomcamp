{{ config(materialized='table') }}


with fhvData as (
    select *
    from {{ ref('stg_fhv_tripdata') }}
), 

dim_zones as (
    select * from {{ ref('dim_zones') }}
    where borough != 'Unknown'
)

select 
    fhvData.*,
    pickup_zone.borough as pickup_borough, 
    pickup_zone.zone as pickup_zone, 
    dropoff_zone.borough as dropoff_borough, 
    dropoff_zone.zone as dropoff_zone,  
   
from fhvData
inner join dim_zones as pickup_zone
on fhvData.pickup_locationid = pickup_zone.locationid
inner join dim_zones as dropoff_zone
on fhvData.dropoff_locationid = dropoff_zone.locationid