from pandas import DataFrame
from sqlalchemy import create_engine, text
from loguru import logger


class SqlLoader:
    def __init__(
        self,
        username: str,
        password: str,
        host: str,
        database: str,
        port: int,
    ):
        """
        Class to help load data to a Sql database

        :param username: database username
        :type username: str
        :param password: database password
        :type password: str
        :param host: database host
        :type host: str
        :param database: database name
        :type database: str
        :param port: database port
        :type port: int
        """
        self._username = username
        self._password = password
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

        :param df: Pandas Dataframe to load
        :type df: DataFrame
        :param table_name: target table name
        :type table_name: str
        :param schema: target schema name, defaults to "public"
        :type schema: str, optional
        """
        engine = create_engine(self.get_uri())

        with engine.connect() as connection:
            logger.info(f"Creating schema {schema} if not exists")
            connection.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema};"))
            connection.commit()

        logger.info(f"Pushing data to {table_name} table")
        logger.debug(
            f"Dataframe: {df}, Table name: {table_name}, Schema: {schema}, If exists: {kwargs.get('if_exists','append')}"
        )
        df.to_sql(
            **kwargs,
            con=engine,
            schema=schema,
            name=table_name,
            index=False,
            if_exists=kwargs.get("if_exists", "append"),
        )
        logger.info(f"Data pushed to {table_name} table")
