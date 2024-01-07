import os
from loguru import logger


class Secrets:
    @staticmethod
    def get(secret_name: str) -> str:
        """
        Get secret from environment

        :param secret_name: secret name
        :type secret_name: str
        :return: secret value
        :rtype: str
        """
        logger.info(f"Getting secret {secret_name} from environment")
        return os.getenv(secret_name)
