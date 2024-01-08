from fire_incidents.loaders.sql_loader import SqlLoader


def test_init():
    # Arrange
    username = "user"
    password = "pass"
    host = "localhost"
    database = "db"
    port = 5432

    # Act
    loader = SqlLoader(username, password, host, database, port)

    # Assert
    assert loader._username == username
    assert loader._password == password
    assert loader.host == host
    assert loader.database == database
    assert loader.port == port
