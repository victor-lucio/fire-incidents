# Fire Incidents

![Python 3.11](https://img.shields.io/badge/python-3.11-blue)
![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)
![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)
![Pre Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-1.7.4-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

This repository contains data and code for analyzing fire incidents. This is my first DBT project, It's meant to work all by itself.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Requirements

- [Docker](https://www.docker.com/), configure with [post-installation steps](https://docs.docker.com/engine/install/linux-postinstall/) to use as a non-root user.
- [Poetry](https://python-poetry.org/) dependency manager.

## Usage

### Makefile

I've set a lot of entries in Makefile, so you will probably just use it.

to spin up the environment:
```make spin-up```
> Make sure you have a copy of profiles.yml if you use it at ~/.dbt, since this command replaces it. The same thing for .pgpass.

to run the raw job:
```make run-load-fire-incidents-raw RUN_DATE=<date-to-run>```

to run dbt models:
```make run-dbt-models```

to tear down stuff you can use:
```make drop-postgres```

---
### How I expect the user to behave

Since we dont have a scheduler like airflow, dagster, or any other cron, we have to do this by hand. It's divided in two parts, the first one is the python extraction of the raw data, that should be ran first.

```make run-load-fire-incidents-raw RUN_DATE=<date-to-run>```

you're gonna see some logs when it's finished, you can try dates like `2010-10-10`.

then run the dbt models to created the clean table and the analysis model

```make run-dbt-models```

now you can check the database to verify how the data is.

```make access-postgres```

- raw data table: `raw.fire_incidents_raw`
- clean table: `dbt_clean.fire_incidents_clean`
- analysis: `dbt_analysis.incidents_by_district_battalion_day`

you can repeat this process changing the date from the raw job execution.

> The dbt models are incremental, they check the last date to update the data
> I didn't put any constraint to repeaded raw data, this must the done in the real world. I'd normally use a datalake in S3 and replace only a partition to maintain idempotency in case of re-running the same job twice. But anyway, the models won't be affected.

---

### About the Code
The project is divided in 2 great folders, that are `dbt` and `fire_incidents`

#### DBT
Here lives all the DBT files, includint the models inside the dbt/models folder, where I defined the `fire_incidents.yml` to define a source and two SQL models

- fire_incidents_clean.sql: the clean transformation for the raw data ingested by the python code
- incidents_by_district_battalion_day.sql: a basic model using the clean data to count number of incidents by district, battalion and day.

#### fire_incidents
Here lives all the python code, it's the main package. It's divided in:
- clients: adapters to get data from
- jobs: where all the scripts to run live
- loaders: adapters to upload data somewhere
- utils: side classes to help us to get secrets, arguments, etc, keeping the main code clean.

#### Comments
1. I used the Socrata SDK for python instead of downloading the CSV or even using the API directly, it's a choice of implementation that should be discussed in the real world, but I found cleaner to use the SDK.

2. I never used DBT before, this is the first time, so I might have missed some good practices, and again, in the real world the files and archtecture should be discussed and probably would be different.

3. I didn't have time to put the effort I wanted to this project, it's missing stuff like more complex CI and a lot of more tests.

### About the Data

I'm gonna describe why I loaded the data like it is.

#### Raw
The raw data has a basic schema to reproduce the data as it comes, we can say that's 'as-is'. I like to do in this way because we can always change how we parse or use the raw data without needing to reprocess that. Another problem that would happen to use the schema with the columns of the source is 'schema evolution', we don't need to bother with that if the entire data is a string. So raw data schema has only a `date` and a json string containing all the data in `data`.

#### Clean
Now it's job for DBT and we select only the columns we need/want, enforcing and checking schema, if something goes wrong in this step, it's gonna be some kind of bad data of type size. We also have the hability of putting any new column from raw that we want from raw and DBT will take care of the evolution for us. Please check the file dbt/models/fire_incidents_clean.sql

#### Analys
Here I created a really simple materialized table to log the number of incidents by some dimensions that could be used in a dashboard or some visualization tool. It's also incremental and uses a composed key to make it work. file at: fire-incidents/dbt/models/incidents_by_district_battalion_day.sql

## Contributing

I'm using pre-commit with ruff library to lint the code.

## License

This project is licensed under the terms of the MIT license.