# -*- coding: utf8 -*-
import unittest
import os
import sys
from Follower import Follower


def Client(**kwargs):
    return APIMock()


def testKwargs(**kwargs):
    return kwargs['kappa']


class APIMock:

    authenticated_user_id = 228
    isMock = True

    def user_info2(self, username):
        return username

    def user_followers(self, user_id, **kwargs):
        end_cursor = kwargs['end_cursor']
        obj = {
            'data': {
                'user': {
                    'edge_followed_by': {
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
            obj['data']['user']['edge_followed_by']['edges'].append({
                'node': {'id': i}
            })
        return obj

    def user_following(self, user_id, **kwargs):
        return self.user_followers(user_id, **kwargs)

    def friendships_create(self, id):
        return id

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
    follower = Follower(Client)
    follower.login = 's'
    follower.password = 'm'

    def test_should_create_fake_api(self):
        # WHEN
        self.follower.get_api()
        # THEN
        self.assertTrue(self.follower.api.isMock)

    def test_should_get_fake_followers(self):
        # when
        self.follower._getFollowers()
        # then
        self.assertTrue(len(self.follower.followers_ids) == 100)

    def testKwargs(self):
        # WHEN
        kappa = testKwargs(kappa=23)
        # THEN
        self.assertEqual(kappa, 23)


if __name__ == '__main__':
    unittest.main()
