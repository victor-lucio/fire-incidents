from pandas import DataFrame
from sqlalchemy import create_engine


class SqlLoader:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        database: str,
        port: int,
    ):
        self.username = username
        self.password = password
        self.host = host
        self.database = database
        self.port = port

    def get_uri(self) -> str:
        """
        Get uri for Sql database
        """
        raise NotImplementedError

    def push_data(
        self, df: DataFrame, table_name: str, schema: str = "public", **kwargs
    ) -> None:
        """
        Push data to Sql database
        """
        engine = create_engine(self.get_uri())
        df.to_sql(
            **kwargs,
            con=engine,
            schema=schema,
            name=table_name,
            index=False,
            if_exists="append",
        )