from fire_incidents.loaders.sql_loader import SqlLoader


class PostgresLoader(SqlLoader):
    def get_uri(self) -> str:
        return f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
