{{
  config(
    materialized='incremental',
    unique_key='id',
    sort='id',
    schema='clean'
  )
}}

select 
  incident_date::date,
  id::int,
  incident_number::int,
  exposure_number::int,
  estimated_contents_loss::int,
  estimated_property_loss::int,
  fire_fatalities::int,
  fire_injuries::int,
  civilian_fatalities::int,
  civilian_injuries::int,
  number_of_alarms::int,
  floor_of_fire_origin::int,
  number_of_floors_with_minimum_damage::int,
  number_of_floors_with_significant_damage::int,
  number_of_floors_with_heavy_damage::int,
  number_of_floors_with_extreme_damage::int,
  number_of_sprinkler_heads_operating::int,
  neighborhood_district::varchar,
  battalion::varchar
from 
  {{ source("raw", "fire_incidents_raw")}}

{% if is_incremental() %}
where 
  incident_date::date > (select max(incident_date) from {{ this }})
{% endif %}