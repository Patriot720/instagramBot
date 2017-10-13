class APIManager():
    def __init__(self, api):
        self.api = api
        self.authenticated_user_id = self.api.authenticated_user_id
        self.api_funcs = {
            "followers": self.api.user_followers,
            "following": self.api.user_following
        }

    def _api_get(self, typeStr, user_id, end_cursor=None, count=1000):
        result = {}
        items = []
        has_next_page = ""
        end_cursor = ""
        if typeStr == 'followers' or typeStr == "following":
            obj = self.api_funcs[typeStr](
                user_id, extract=False, end_cursor=end_cursor, count=1000)
            edge = obj['data']['user'].popitem()[1]
            end_cursor = edge['page_info']['end_cursor']
            has_next_page = edge['page_info']['has_next_page']
            items = edge['edges']
        elif typeStr == "tag_feed":
            obj = self.api.tag_feed(user_id, max_id=end_cursor, count=count)
            media = obj['tag']['media']
            has_next_page = media['page_info']['has_next_page']
            max_id = media['page_info']['end_cursor']
            items = media['nodes']
        result["end_cursor"] = end_cursor
        result["has_next_page"] = has_next_page
        result["items"] = items
        return result

    def _process_api_obj(self, obj):
        result = {}
        items = []
        has_next_page = ""
        end_cursor = ""

        return result

    def friendships_destroy(self, user):
        self.api.friendships_destroy(user)

    def friendships_create(self, user):
        self.api.friendships_create(user)

    def get(self, typeStr, user_id, count=5000):
        ids = []
        has_next_page = True
        count = count
        end_cursor = None
        while(has_next_page and len(ids) < count):
            res = self._api_get(typeStr,
                                user_id, end_cursor=end_cursor, count=count)
            end_cursor = res['end_cursor']
            has_next_page = res['has_next_page']
            items = res['items']
            for item in items:
                ids.append(item.popitem()[1]['id'])
        return ids

    def get_user_id(self, username):
        user = self.api.user_info2(username)
        return user['id']
