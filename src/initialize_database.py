from database_connection import get_database_connection


def drop_tables(connection):
    """Poistaa suoritusta häiritsevän taulun

    Args:
        connection: yhteys tietokantaan
    """
    cursor = connection.cursor()
    cursor.execute('''
        drop table if exists Scores;
    ''')
    connection.commit()


def create_tables(connection):
    """Luo oikeat taulut

    Args:
        connection: yhteys tietokantaan
    """
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE Scores (id INTEGER PRIMARY KEY, username TEXT, difficulty INTEGER, time REAL)"
        )
    connection.commit()

def initialize_database():
    """Alustaa tietokannan, eli luo sen jos puuttuu ja nollaa taulut
    """
    #taulu luodaan tarvittaessa tällä
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
