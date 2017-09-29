import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError
from APIManager import APIManager
from PyQt5.QtCore import QObject, pyqtSignal


def rand(max_range=10000):
    return random.randint(0, max_range)


def mockClient(**kwargs):
    if(kwargs['settings'] or (kwargs['username'] != "empty" and kwargs['password'] != "empty")):
        api = APIMock()
        if(kwargs["on_login"]):
            kwargs["on_login"](api)
        return api
    else:
        raise ClientError("Wrong shiet")


class mockFollower(QObject):
    api_end = pyqtSignal(str)
    end = pyqtSignal(str)
    mid = pyqtSignal(str)
    SAMPLE_MSG = "SAMPLE_MSG"

    def __init__(self):
        super().__init__()
        self.funcs = [
            self.func1,
            self.func2
        ]

    def start(self):
        self.started = True
        self.funcs[self.index]()
        self.end.emit(self.SAMPLE_MSG)
        return

    def func1(self):
        self.func1_launched = True

    def func2(self):
        self.func2_launched = True

    def set_index(self, index):
        self.index = index

    def set_name(self, name):
        self.name = name

    def stop(self):
        self.stopped = True
        return


class APIMock:
    authenticated_user_id = 228
    isMock = True

    def __init__(self):
        self.ids = []
        self.settings = "%%"

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
