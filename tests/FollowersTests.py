# -*- coding: utf8 -*-
import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Follower import Follower
from SubsManager import SubsManager
from MockClasses import *
import random


def sleepfunc():
    return


class TestFollowers(unittest.TestCase):
    def setUp(self):
        self.api = SubsManager(APIMock())
        follower = Follower(self.api)
        self.follower = follower
        self.follower.set_sleep_function(sleepfunc)
        self.id = self.api.authenticated_user_id

    def test_should_have_followers_on_init(self):
        # THEN
        self.assertTrue(len(self.follower.followers))

    def test_should_remove_followings(self):
        # WHEN
        self.follower._remove_following('')
        # THEN
        self.assertTrue(len(self.follower.api.api.ids))

    def test_should_test_viable_id(self):
        # WHEN
        viable = self.follower._is_viable(self.id)
        self.assertTrue(viable)

    def test_should_follow_subs_by_username(self):
        # WHEN
        self.follower._follow_subs_by_username("username")
        # THEN
        self.assertTrue(len(self.follower.api.api.ids))

    def test_should_follow_subs_by_hastag(self):
        # when
        self.follower._follow_subs_by_hashtag("kappa")
        # then
        self.assertTrue(len(self.follower.api.api.ids))

    def test_should_follow_by_hashtag(self):
        # when
        self.follower._follow_by_hashtag("kappa")
        # then
        self.assertTrue(len(self.follower.api.api.ids))


if __name__ == '__main__':
    unittest.main()
