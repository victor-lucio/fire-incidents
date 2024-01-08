from unittest.mock import patch
from fire_incidents.clients.socrata_client import SocrataClient
from sodapy import Socrata


@patch.object(Socrata, "__init__")
def test_init(mock_socrata):
    mock_socrata.return_value = None
    SocrataClient("data.sfgov.org")
    mock_socrata.assert_called_once()


@patch.object(Socrata, "get_all")
def test_get_data(mock_socrata):
    mock_dataset = "wr8u-xric"
    mock_filters = {"limit": 5000, "offset": 0}
    mock_return_value = [{"column1": "value1"}, {"column2": "value2"}]
    mock_socrata.return_value = mock_return_value

    client = SocrataClient("data.sfgov.org")
    result = client.get_data(mock_dataset, **mock_filters)

    mock_socrata.assert_called_once_with(mock_dataset, **mock_filters)
    assert result == mock_return_value
