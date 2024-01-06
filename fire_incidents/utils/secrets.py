import os


class Secrets:
    @staticmethod
    def get(secret_name: str):
        return os.getenv(secret_name)
