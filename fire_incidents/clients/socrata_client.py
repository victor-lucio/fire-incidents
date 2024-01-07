from sodapy import Socrata
from loguru import logger


class SocrataClient:
    """
    Socrata client to get data from Socrata API using provided SDK

    https://pypi.org/project/sodapy/
    """

    def __init__(self, domain: str) -> None:
        """Contructor

        :param domain: The domain of the Socrata API (e.g. data.sfgov.org)
        :type domain: str
        """
        logger.info("Initializing Socrata client")
        self._client = Socrata(domain, None)

    def get_data(self, dataset: str, **filters) -> list:
        """Get data from Socrata API

        :param dataset: The dataset to get data from (e.g. wr8u-xric)
        :type dataset: str
        :return: data from Socrata API in a list of dictionaries
        :rtype: list
        """
        logger.info(f"Getting data from {dataset} dataset")
        return self._client.get_all(dataset, **filters)
