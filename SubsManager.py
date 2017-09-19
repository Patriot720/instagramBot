class SubsManager():
    def __init__(self, api):
        self.api = api
        self.authenticated_user_id = self.api.authenticated_user_id

    def get(self, typeStr, user_id):
        ids = []
        edge_type = self._select_edge(typeStr)
        if(not edge_type):
            return
        has_next_page = True
        end_cursor = None
        while(has_next_page):
            following = self._api_get(typeStr,
                                      user_id, extract=False, end_cursor=end_cursor, count=1000)
            edge = following['data']['user'][edge_type]
            end_cursor = edge['page_info']['end_cursor']
            has_next_page = edge['page_info']['has_next_page']
            users = edge['edges']
            for user in users:
                ids.append(user['node']['id'])
        return ids

    def _select_edge(self, typeStr):
        if typeStr == "followers":
            return 'edge_followed_by'
        if typeStr == "following":
            return 'edge_follow'
        return False

    def _api_get(self, typeStr, user_id, extract=False, end_cursor=None, count=1000):
        if typeStr == 'followers':
            return self.api.user_followers(
                user_id, extract=False, end_cursor=end_cursor, count=1000)
        if typeStr == 'following':
            return self.api.user_following(
                user_id, extract=False, end_cursor=end_cursor, count=1000)

    def friendships_destroy(self, user):
        self.api.friendships_destroy(user)

    def friendships_create(self, user):
        self.api.friendships_create(user)

    def get_user_ids_from_tag_feed(self, hashtag, end_cursor=None, count=1000):
        ids = []
        max_id = None
        count = count
        has_next_page = True
        while(has_next_page):
            res = self.api.tag_feed(hashtag, max_id=max_id, count=count)
            media = res['tag']['media']
            has_next_page = media['page_info']['has_next_page']
            max_id = media['page_info']['end_cursor']
            items = media['nodes']
            for item in items:
                ids.append(item['owner']['id'])
        return ids

    def get_user_id(self, username):
        user = self.api.user_info2(username)
        return user['id']
