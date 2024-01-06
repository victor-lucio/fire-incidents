from sodapy import Socrata


class SocrataClient:
    """
    https://pypi.org/project/sodapy/
    """

    def __init__(self, domain: str) -> None:
        self._client = Socrata(domain, None)

    def get_data(self, dataset: str, **filters) -> list:
        """
        Get data from dataset
        """
        return self._client.get_all(dataset, **filters)
