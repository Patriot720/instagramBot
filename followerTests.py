# -*- coding: utf8 -*-
import unittest
import os
import sys
from Follower import Follower
import random


def Client(**kwargs):
    return APIMock()


def testKwargs(**kwargs):
    return kwargs['kappa']


def sleepfunc():
    return


class APIMock:
    ids = []
    authenticated_user_id = 228
    isMock = True

    def user_info2(self, username):
        return username

    def user_followers(self, user_id, following=False, **kwargs):
        end_cursor = kwargs['end_cursor']
        edge = 'edge_followed_by'
        if(following):
            edge = 'edge_follow'
        obj = {
            'data': {
                'user': {
                    edge: {
                        'page_info': {
                            'end_cursor': 25,
                            'has_next_page': False if end_cursor else True
                        },
                        'edges': []
                    }
                }
            }
        }
        for i in range(kwargs['count']):
            obj['data']['user'][edge]['edges'].append({
                'node': {'id': random.randint(0, 10000)}
            })
        return obj

    def user_following(self, user_id, **kwargs):
        return self.user_followers(user_id, following=True, **kwargs)

    def friendships_create(self, id):
        return self.ids.append(id)

    def friendships_destroy(self, id):
        return self.ids.append(id)

    def tag_feed(hastag, **kwargs):
        obj = {
            'tag': {
                'media': {
                    'page_info': {
                        'has_next_page': 0,
                        'end_cursor': 'kappa'
                    },
                    'nodes': {
                        'owner': {
                            'id': 228
                        }

                    }
                }
            }
        }


class TestFollowers(unittest.TestCase):
    def setUp(self):
        follower = Follower(Client)
        follower.login = 's'
        follower.password = 'm'
        self.follower = follower

    def test_should_create_fake_api(self):
        # WHEN
        self.follower.get_api()
        # THEN
        self.assertTrue(self.follower.api.isMock)

    def test_should_get_fake_followers(self):
        # when
        self.follower._get('followers')
        # then
        self.assertEqual(len(self.follower.ids['followers']), 2000)

    def test_should_get_fake_following(self):
        # WHEN
        self.follower._get('following')
        # then
        self.assertEqual(len(self.follower.ids['following']), 2000)

    def testKwargs(self):
        # WHEN
        kappa = testKwargs(kappa=23)
        # THEN
        self.assertEqual(kappa, 23)

    def test_should_remove_followings(self):
        # WHEN
        self.follower.setSleepFunction(sleepfunc)
        self.follower.removeFollowing('')
        # THEN
        self.assertEqual(len(self.follower.api.ids),
                         len(self.follower.ids['following']))


if __name__ == '__main__':
    unittest.main()
