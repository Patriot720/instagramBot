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
            following = self._apiGet(typeStr,
                                     user_id, extract=False, end_cursor=end_cursor, count=1000)
            edge = following['data']['user'][edge_type]
            end_cursor = edge['page_info']['end_cursor']
            has_next_page = edge['page_info']['has_next_page']
            users = edge['edges']

            for user in users:
                ids.append(user['node']['id'])
        return ids

    def _apiGet(self, typeStr, user_id, extract=False, end_cursor=None, count=1000):
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

    def tag_feed(self, hashtag, count=1000):
        return

    def get_user_id(self, username):
        user = self.api.user_info2(username)
        return user['id']

    def _select_edge(self, typeStr):
        if typeStr == "followers":
            return 'edge_followed_by'
        if typeStr == "following":
            return 'edge_follow'
        return False
