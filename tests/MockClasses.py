import random


def rand(max_range=10000):
    return random.randint(0, max_range)


class APIMock:
    ids = []
    authenticated_user_id = 228
    isMock = True

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
        end_cursor = kwargs['end_cursor']
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
        for i in range(1000):
            obj['tag']['media']['nodes'].append({
                'owner': {'id': rand()}
            })
        return obj
