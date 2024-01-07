{{
  config(
    materialized='incremental',
    unique_key="sk",
    sort='incident_date',
    schema='analysis'
  )
}}

select
    incident_date||'-'||neighborhood_district||'-'||battalion as sk,
    incident_date,
    neighborhood_district,
    battalion,
    count(*) as incident_count
from {{ ref('fire_incidents_clean') }}
{% if is_incremental() %}
where
    incident_date > (select max(incident_date) from {{ this }})
{% endif %}
group by 1,2,3,4
