import random
from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from APIManager import APIManager


def rand(max_range=10000):
    return random.randint(0, max_range)


class APIMock:
    authenticated_user_id = 228
    isMock = True

    def __init__(self):
        self.ids = []

    def user_info2(self, username):
        return {'id': rand()}

    def user_followers(self, user_id, following=False, count=1000, **kwargs):
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
        for i in range(count):
            obj['data']['user'][edge]['edges'].append({
                'node': {'id': rand()}
            })
        return obj

    def user_following(self, user_id, **kwargs):
        return self.user_followers(user_id, following=True, **kwargs)

    def friendships_create(self, id):
        return self.ids.append(id)

    def friendships_destroy(self, id):
        return self.ids.append(id)

    def tag_feed(self, hastag, **kwargs):
        end_cursor = kwargs['max_id']
        count = kwargs['count']
        obj = {
            'tag': {
                'media': {
                    'page_info': {
                        'has_next_page': False if end_cursor else True,
                        'end_cursor': 1
                    },
                    'nodes': []
                }
            }
        }
        for i in range(count):
            obj['tag']['media']['nodes'].append({
                'owner': {'id': rand()}
            })
        return obj

class APIMockWithRealApi(APIMock):
    def __init__(self):
        super().__init__()
        self.api = Client(auto_patch=True, authenticate=True,
                          username="patriotdoto", password="Pp4991342446")
        self.authenticated_user_id = self.api.authenticated_user_id

    def user_followers(self, user_id, following=False, count=1000, **kwargs):
        end_cursor = kwargs['end_cursor']
        count = count
        return self.api.user_followers(user_id, extract=False, max_id=end_cursor, count=count)

    def user_following(self, user_id, following=False, count=1000, **kwargs):
        end_cursor = kwargs['end_cursor']
        count = count
        return self.api.user_following(user_id, extract=False, max_id=end_cursor, count=count)
