from sodapy import Socrata
from loguru import logger


class SocrataClient:
    """
    Socrata client to get data from Socrata API using provided SDK

    https://pypi.org/project/sodapy/
    """

    def __init__(self, domain: str) -> None:
        """_summary_

        :param domain: _description_
        :type domain: str
        """
        logger.info("Initializing Socrata client")
        self._client = Socrata(domain, None)

    def get_data(self, dataset: str, **filters) -> list:
        """_summary_

        :param dataset: _description_
        :type dataset: str
        :return: _description_
        :rtype: list
        """
        logger.info(f"Getting data from {dataset} dataset")
        return self._client.get_all(dataset, **filters)
