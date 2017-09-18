# -*- coding: utf8 -*-
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# import ../db.py
from Follower import Follower
import unittest


def Client(**kwargs):
    return APIMock()

class APIMock:

    authenticated_user_id = 228
    isMock = True
    def user_info2(self, username):
        return username

    def user_followers(self, user_id,extract=None, end_cursor=None, count=None):
        arr = []
        obj = {
            'data':{
                'user':{
                    'edge_followed_by':{
                        'page_info':{
                            'end_cursor': 1,
                            'has_next_page': False
                        },
                        'edges':[]
                    }
                }
            }
        }
        for i in range(100):
            obj['data']['user']['edge_followed_by']['edges'].append({
                'node':{'id': i}
            })
        return obj
    def user_following(self,user_id,max_id=None,count=None):
        return self.user_followers(user_id)
    def friendships_create(self,id):
        return id
    def tag_feed(hastag,max_id=None):
        obj = {
            'tag':{
                'media':{
                    'page_info':{
                        'has_next_page': 0,
                        'end_cursor': 'kappa'
                    },
                    'nodes':{
                        'owner':{
                            'id':228
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
        #WHEN
        self.follower.get_api()
        #THEN
        self.assertTrue(self.follower.api.isMock)
    def test_should_get_fake_followers(self):
        #when
        self.follower._getFollowers()
        #then
        self.assertTrue(len(self.follower.followers_ids) == 100)
        
    
if __name__ == '__main__':
    unittest.main()