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
        self.follower.setSleepFunction(sleepfunc)
        self.id = self.api.authenticated_user_id

    def test_should_remove_followings(self):
        # WHEN
        self.follower.removeFollowing('')
        # THEN
        self.assertTrue(len(self.follower.api.api.ids))

    def test_should_test_viable_id(self):
        # WHEN
        viable = self.follower._is_viable(self.id)
        self.assertTrue(viable)

    # def test_should_follow_subs_by_username(self):
    #     # WHEN
    #     self.follower._follow_subs_by_username("username")
    #     # THEN
    #     self.assertTrue(1)


if __name__ == '__main__':
    unittest.main()
