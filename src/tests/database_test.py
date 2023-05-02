from repository.leaderboard_repository import LeaderboardRepository
import database_connection
import initialize_database
import unittest

class TestLeaderboardRepository(unittest.TestCase):
    def setUp(self) -> None:
        initialize_database.initialize_database()
        connection = database_connection.get_database_connection()
        self.leaderboard_repository = LeaderboardRepository(connection)

    def test_can_add_entry(self):
        self.leaderboard_repository.add_score("name", 0, 2)
        self.assertEqual(len(self.leaderboard_repository.get_scores(0)), 1)

    def test_entries_are_sorted(self):
        self.leaderboard_repository.add_score("name", 0, 2)
        self.leaderboard_repository.add_score("name", 0, 1)
        self.assertEqual(self.leaderboard_repository.get_scores("0")[0], ("name", "0", "1"))

    def test_returns_only_ten_or_fewer(self):
        for i in range(20):
            self.leaderboard_repository.add_score("name", 0, 2)
        self.assertEqual(len(self.leaderboard_repository.get_scores(0)), 10)

    def test_can_filter_by_difficulty(self):
        self.leaderboard_repository.add_score("name", 0, 2)
        self.leaderboard_repository.add_score("name", 1, 2)
        self.assertEqual(len(self.leaderboard_repository.get_scores(1)), 1)