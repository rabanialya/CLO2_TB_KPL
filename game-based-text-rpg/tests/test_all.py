import sys
import os
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import dari project
from client.game_client import Player, Enemy, Location, battle
from main import app
from fastapi.testclient import TestClient

# === UNIT TEST BAGIAN GAME ===
class TestGame(unittest.TestCase):
    def setUp(self):
        self.player = Player("TestHero", "Mage", 100, 25)
        self.enemy = Enemy("Goblin", 50, 10)
        self.location = Location("Test Cave", "Tempat uji coba", enemies=["Goblin"])

    def test_player_attack_enemy(self):
        self.player.attack_enemy(self.enemy)
        self.assertLess(self.enemy.hp, 50)

    def test_enemy_attack_player(self):
        self.enemy.attack_player(self.player)
        self.assertLess(self.player.hp, 100)

    def test_use_item(self):
        self.player.hp = 50
        self.player.items = [{"name": "Potion", "heal": 30}]
        with patch("builtins.input", return_value="1"):
            self.player.use_item()
        self.assertEqual(self.player.hp, 80)
        self.assertEqual(len(self.player.items), 0)

    def test_battle_win(self):
        with patch("builtins.input", side_effect=["1"] * 10):
            result = battle(self.player, self.enemy, self.location)
        self.assertTrue(result)

# === INTEGRATION TEST FASTAPI ===
class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "API ready"})

    def test_get_jobs(self):
        response = self.client.get("/jobs")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Warrior", response.json())

    def test_get_items(self):
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Potion", response.json())

    def test_get_enemies(self):
        response = self.client.get("/enemies")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Goblin", response.json())

    def test_get_locations(self):
        response = self.client.get("/locations")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Village", response.json())

# === RUNNER ===
if __name__ == '__main__':
    unittest.main()