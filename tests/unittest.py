import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Ensure app is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Auth utility tests
from app.auth import Auth, AuthToken

class TestAuthUtils(unittest.TestCase):
    def setUp(self):
        self.token = AuthToken()

    def test_generate_random_string_length(self):
        s = self.token.generateRandomString(10)
        self.assertEqual(len(s), 10)
        self.assertTrue(all(c.isalnum() for c in s))

    def test_sha256(self):
        digest = self.token.sha256("test")
        self.assertEqual(len(digest), 32)  # SHA256 digest is 32 bytes

    def test_base64encode(self):
        raw = b"\x00" * 32
        encoded = self.token.base64encode(raw)
        self.assertIsInstance(encoded, str)
        self.assertNotIn("=", encoded)
        self.assertNotIn("+", encoded)
        self.assertNotIn("/", encoded)

    def test_generate_code_challenge(self):
        verifier = self.token.generateRandomString(128)
        challenge = self.token.generateCodeChallenge(verifier)
        self.assertIsInstance(challenge, str)
        self.assertTrue(len(challenge) > 0)

# Util function tests
from app.util import (
    validate_password,
    validate_username,
    validate_email,
    validate_score
)

class TestUtil(unittest.TestCase):

    def test_validate_password(self):
        cases = [
            ("Password1@", None, None),
            ("pass1@", None, "Password must contain at least 1 letter, 1 number, and 1 special character."),
            ("Password1", None, "Password must contain at least 1 letter, 1 number, and 1 special character."),
            ("Password@", None, "Password must contain at least 1 letter, 1 number, and 1 special character."),
            ("12345678@", None, "Password must contain at least 1 letter, 1 number, and 1 special character."),
            ("Password1@", "Password1@", None),
            ("Password1@", "Password2@", "Confirmed passwords do not match."),
        ]
        for password, confirm, expected in cases:
            self.assertEqual(validate_password(password, confirm), expected)

    def test_validate_username(self):
        cases = [
            ("user_1", None),
            ("us", "Invalid username. Use letters, numbers, underscores only."),
            ("user$", "Invalid username. Use letters, numbers, underscores only."),
            ("user name", "Invalid username. Use letters, numbers, underscores only."),
            ("username", None),
            ("user123", None),
        ]
        for username, expected in cases:
            self.assertEqual(validate_username(username), expected)

    def test_validate_email(self):
        cases = [
            ("test@example.com", None),
            ("test.email+alex@leetcode.com", None),
            ("test.email@sub.domain.com", None),
            ("test.email@", "Invalid email address"),
            ("test@.com", "Invalid email address"),
            ("test.com", "Invalid email address"),
        ]
        for email, expected in cases:
            self.assertEqual(validate_email(email), expected)

    def test_validate_score_valid(self):
        cases = [
            ("", ""),  # deletion
            ("10", "10"),
            ("9", "9"),
            ("8.5", "8.5"),
            ("7.25", "7.25"),
            ("10.0", "10"),
            ("10.01", "10"),  # Should cap at 10
            ("0", "0"),
            ("0.00", "0.0"),
        ]
        for score, expected in cases:
            self.assertEqual(validate_score(score), expected)

    def test_validate_score_invalid(self):
        invalid_scores = [
            "11",
            "abc",
            "8..5",
            "8.5.1",
            "8.a",
            "a.5",
        ]
        for score in invalid_scores:
            with self.assertRaises(ValueError):
                validate_score(score)

# Item class tests
from app.item import Item

class TestItem(unittest.TestCase):
    @patch("app.item.current_user")
    def test_init_track(self, mock_current_user):
        mock_current_user.user_id = 1
        data = {
            "id": "track1",
            "type": "track",
            "name": "Song Title",
            "album": {
                "name": "Album Name",
                "id": "album1",
                "images": [{"url": "http://img.com/1.jpg"}]
            },
            "artists": [
                {"id": "artist1", "name": "Artist One"},
                {"id": "artist2", "name": "Artist Two"}
            ]
        }
        item = Item(data)
        self.assertEqual(item.id, "track1")
        self.assertEqual(item.type, "track")
        self.assertEqual(item.title, "Song Title")
        self.assertEqual(item.album, "Album Name")
        self.assertEqual(item.album_id, "album1")
        self.assertEqual(item.img_url, "http://img.com/1.jpg")
        self.assertEqual(item.artist_ids, ["artist1", "artist2"])
        self.assertEqual(item.creator, "Artist One, Artist Two")

    @patch("app.item.current_user")
    def test_init_album(self, mock_current_user):
        mock_current_user.user_id = 2
        data = {
            "id": "album1",
            "type": "album",
            "name": "Album Title",
            "images": [{"url": "http://img.com/2.jpg"}],
            "artists": [
                {"id": "artist1", "name": "Artist One"}
            ]
        }
        item = Item(data)
        self.assertEqual(item.type, "album")
        self.assertEqual(item.img_url, "http://img.com/2.jpg")
        self.assertEqual(item.artist_ids, ["artist1"])
        self.assertEqual(item.creator, "Artist One")

    @patch("app.item.current_user")
    def test_init_artist(self, mock_current_user):
        mock_current_user.user_id = 3
        data = {
            "id": "artist1",
            "type": "artist",
            "name": "Artist Name",
            "images": [{"url": "http://img.com/3.jpg"}]
        }
        item = Item(data)
        self.assertEqual(item.type, "artist")
        self.assertEqual(item.img_url, "http://img.com/3.jpg")
        self.assertEqual(item.artist_ids, ["artist1"])
        self.assertEqual(item.creator, "Artist Name")

    def test_init_from_database(self):
        class Dummy:
            score = "8"
            item_id = "track2"
            item_type = "track"
            title = "DB Song"
            creator = "DB Artist"
            img_url = "http://img.com/db.jpg"
            album = "DB Album"
            album_id = "db_album"
            artist_ids = "a1,a2"
        item = Item(Dummy(), from_db=True)
        self.assertEqual(item.score, "8")
        self.assertEqual(item.id, "track2")
        self.assertEqual(item.artist_ids, ["a1", "a2"])

    def test_to_dict(self):
        class Dummy:
            score = "7"
            item_id = "track3"
            item_type = "track"
            title = "Dict Song"
            creator = "Dict Artist"
            img_url = "http://img.com/dict.jpg"
            album = "Dict Album"
            album_id = "dict_album"
            artist_ids = "b1,b2"
        item = Item(Dummy(), from_db=True)
        d = item.to_dict()
        self.assertEqual(d["id"], "track3")
        self.assertEqual(d["score"], "7")
        self.assertEqual(d["artist_ids"], ["b1", "b2"])

    def test_stringify_artist_ids(self):
        ids = ["a", "b", "c"]
        result = Item.stringify_artist_ids(ids)
        self.assertEqual(result, "a,b,c")

# Integration tests
from app import create_app, db
from app.config import TestingConfig
from app.models import User

class TestRoutesIntegration(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        super().tearDown()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Home', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_successful_user_creation(self):
        user = User(username="testuser", email="test@example.com", password="hashedpw")
        db.session.add(user)
        db.session.commit()
        found = User.query.filter_by(username="testuser").first()
        self.assertIsNotNone(found)
        self.assertEqual(found.email, "test@example.com")

if __name__ == "__main__":
    unittest.main()
