import os
import sqlite3
from config import LEADERBOARD_REPO

dirname = os.path.dirname(__file__)

connection = sqlite3.connect(os.path.join(dirname, "repository", "data", LEADERBOARD_REPO))
connection.row_factory = sqlite3.Row


def get_database_connection():
    """Tarvittaessa luo tiedoston ja palauttaa viitteen siihen

    Returns:
        connection: tietokantaan viittaava yhteys
    """
    return connection
