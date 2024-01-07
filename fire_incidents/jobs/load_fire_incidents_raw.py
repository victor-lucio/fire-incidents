from fire_incidents.clients.socrata_client import SocrataClient
from fire_incidents.loaders.postgres_loader import PostgresLoader
from fire_incidents.utils.argparse import get_default_args
from pandas import DataFrame

from fire_incidents.utils.secrets import Secrets

DOMAIN = "data.sfgov.org"
DATASET = "wr8u-xric"
DATE_COL = "incident_date"


class LoadFireIncidentRaw:
    def __init__(self, **args) -> None:
        self.args = args
        self.run_date = args.get("run_date")

    def run(self) -> None:
        # Get data from Socrata
        client = SocrataClient(DOMAIN)
        data = client.get_data(
            DATASET, where=f"{DATE_COL}='{self.run_date}T00:00:00'"
        )

        # Convert to DataFrame, force string type
        data_df = DataFrame(data, dtype=str)

        # Load data
        loader = PostgresLoader(
            username=Secrets.get("POSTGRES_USERNAME"),
            password=Secrets.get("POSTGRES_PASSWORD"),
            host=Secrets.get("POSTGRES_HOST"),
            database=Secrets.get("POSTGRES_DATABASE"),
            port=5432,
        )
        loader.push_data(data_df, table_name="fire_incidents_raw", schema="raw")


if __name__ == "__main__":
    args = vars(get_default_args())
    LoadFireIncidentRaw(**args).run()
