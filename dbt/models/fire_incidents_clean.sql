{{
  config(
    materialized='incremental',
    unique_key='id',
    sort='id',
    schema='clean'
  )
}}

with source as (
  select
    data::json as data,
    date::date as date
  from
    {{ source("raw", "fire_incidents_raw") }}

  {% if is_incremental() %}
  where
    date > (select max(incident_date) from {{ this }})
  {% endif %}
)

select 
  (data->>'incident_date')::date as incident_date,
  (data->>'id')::int as id,
  (data->>'incident_number')::int as incident_number,
  (data->>'exposure_number')::int as exposure_number,
  (data->>'estimated_contents_loss')::int as estimated_contents_loss,
  (data->>'estimated_property_loss')::int as estimated_property_loss,
  (data->>'fire_fatalities')::int as fire_fatalities,
  (data->>'fire_injuries')::int as fire_injuries,
  (data->>'civilian_fatalities')::int as civilian_fatalities,
  (data->>'civilian_injuries')::int as civilian_injuries,
  (data->>'number_of_alarms')::int as number_of_alarms,
  (data->>'floor_of_fire_origin')::int as floor_of_fire_origin,
  (data->>'number_of_floors_with_minimum_damage')::int as number_of_floors_with_minimum_damage,
  (data->>'number_of_floors_with_significant_damage')::int as number_of_floors_with_significant_damage,
  (data->>'number_of_floors_with_heavy_damage')::int as number_of_floors_with_heavy_damage,
  (data->>'number_of_floors_with_extreme_damage')::int as number_of_floors_with_extreme_damage,
  (data->>'number_of_sprinkler_heads_operating')::int as number_of_sprinkler_heads_operating,
  (data->>'neighborhood_district')::varchar as neighborhood_district,
  (data->>'battalion')::varchar as battalion
from 
  source