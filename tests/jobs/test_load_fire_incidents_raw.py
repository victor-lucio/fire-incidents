from unittest.mock import patch

from fire_incidents.clients.socrata_client import SocrataClient
from fire_incidents.jobs.load_fire_incidents_raw import LoadFireIncidentRaw
from fire_incidents.loaders.postgres_loader import PostgresLoader
from pandas import DataFrame


@patch.object(PostgresLoader, "push_data")
@patch.object(SocrataClient, "get_data")
def test_run(mock_get_data, mock_push_data):
    source_date = [
        {"col1": "value1", "col2": "value2", "incident_date": "2022-01-01T00:00:00"},
        {"col1": "value3", "col2": "value4", "incident_date": "2022-01-01T00:00:00"},
    ]

    expected_data = [
        {
            "data": '{"col1": "value1", "col2": "value2", "incident_date": "2022-01-01T00:00:00"}',
            "date": "2022-01-01T00:00:00",
        },
        {
            "data": '{"col1": "value3", "col2": "value4", "incident_date": "2022-01-01T00:00:00"}',
            "date": "2022-01-01T00:00:00",
        },
    ]

    mock_get_data.return_value = source_date

    LoadFireIncidentRaw(run_date="2022-01-01").run()

    assert DataFrame(expected_data).equals(mock_push_data.call_args_list[0][0][0])
