class LeaderboardRepository:
    """Luokka toimii GameFramen ja tietokannan rajapintana, tallentaa ja lukee tietokantaa

    Attributes:
        connection: viittaa tietokantaan, jota käytetään
    """
    def __init__(self, connection):
        """Konstruktori jolle annetaan tietokantaan viittaava yhteys

        Args:
            connection: tietokanta
        """
        self._connection = connection

    def get_scores(self, difficulty):
        """Lukee halutun vaikeustason tuloksia

        Args:
            difficulty int: vaikeustaso jonka tulokset palautetaan

        Returns:
            list: lista tuloksista
        """
        cursor = self._connection.cursor()
        if difficulty == 0:
            cursor.execute("SELECT * FROM Scores ORDER BY time LIMIT 10")
        else:
            cursor.execute(
                "SELECT * FROM Scores WHERE difficulty=? ORDER BY time LIMIT 10",
                [difficulty]
                )
        rows = cursor.fetchall()
        return [(row["username"], row["difficulty"], row["time"]) for row in rows]

    def add_score(self, name, diff, time):
        """Lisää tuloksen tietokantaan

        Args:
            name str: käyttäjän syöttämä nimi
            diff int: vaikeustaso jolla pelattiin
            time float: aika joka peliin kesti sekunneissa
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO Scores (username, difficulty, time) VALUES (?,?,?)",
            [name,diff,time]
            )
        self._connection.commit()
