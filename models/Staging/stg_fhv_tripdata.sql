{{ config(materialized='view') }}

select
dispatching_base_num, 
cast(pickup_datetime as timestamp) as pickup_datetime,
cast(dropOff_datetime as timestamp) as dropOff_datetime,
cast(pulocationid as integer) as  pickup_locationid,
cast(dolocationid as integer) as dropoff_locationid,
SR_Flag,
Affiliated_base_number

from {{ source('staging','fhv_tripdata_2019_BQ') }}

