import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SubsManager import SubsManager
import random
from MockClasses import *


class TestFollowers(unittest.TestCase):
    def setUp(self):
        self.api = APIMock()
        subsManager = SubsManager(self.api)
        self.subsManager = subsManager
        self.id = self.api.authenticated_user_id

    def test_should_get_fake_followers(self):
        # given
        # when
        ids = self.subsManager.get('followers', self.id)
        # then
        self.assertEqual(len(ids), 2000)

    def test_should_get_fake_followings(self):
        # when
        ids = self.subsManager.get('following', self.id)
        # then
        self.assertEqual(len(ids), 2000)

    def test_should_get_fake_tag_feed_users(self):
        # when
        ids = self.subsManager.get_user_ids_from_tag_feed("hashtag")
        # then
        self.assertEqual(len(ids), 2000)


if __name__ == "__main__":
    unittest.main()
