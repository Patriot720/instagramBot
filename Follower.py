# -*- coding: utf8 -*-
from PyQt5.QtCore import QObject, pyqtSignal
import os.path
import time
from urllib.error import (HTTPError)
from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError

SLEEP_TIME = 60
SLEEP_TIME_MODULE = 60
STANDART_STOP_MESSAGE = "Остановлено"


class Follower(QObject):
    api_end = pyqtSignal(str)
    end = pyqtSignal(str)
    mid = pyqtSignal(str)

    def __init__(self, client=Client):
        super().__init__()
        self.client = client
        if(os.path.isfile("ignoreList.txt")):
            ignore = open("ignoreList.txt", 'r')
            self.ignore_list = ignore.read().splitlines()
            ignore.close()
        else:
            self.ignore_list = []
        self.functions = [
            self._follow_subs_by_username,
            self._follow_subs_by_hashtag,
            self._follow_by_hashtag,
            self.removeFollowing
        ]
        self._isRunning = True
        self.ids = {
            'followers': [],
            'following': []
        }

    def follow(self):
        try:
            self.functions[self.index](self.text)
        except ClientError as e:
            self.end.emit("Instagram блочит или неверный ник/тег")
        except ValueError:
            self.end.emit("Неверный ник/тег")
        except HTTPError:
            self.end.emit("Слишком много запросов, придется подождать")

    def removeFollowing(self, name):
        self._get('following')
        self.mid.emit('Скачал все подписки')
        self._get('followers')
        self.ids['followers'] = []
        self.mid.emit('Скачал всех подписчиков')
        for user in self.ids['following']:
            if(user not in self.ids['followers']):
                self.api.friendships_destroy(user)
                self.mid.emit("Удалил" + str(user))
                self._sleep()
        self.end.emit("Завершено")

    def setSleepFunction(self, func):
        self.sleep = func

    def _sleep(self):
        for i in range(SLEEP_TIME_MODULE):
            if(not self._isRunning):
                self.end.emit(STANDART_STOP_MESSAGE)
                return
            time.sleep(SLEEP_TIME / SLEEP_TIME_MODULE)

    def _get(self, typeStr):
        self.ids[typeStr] = []
        if typeStr == "followers":
            edge_type = 'edge_followed_by'

        elif typeStr == "following":
            edge_type = 'edge_follow'
        else:
            return
        has_next_page = True
        end_cursor = None
        while(has_next_page):
            following = self._apiGet(typeStr,
                                     self.id, extract=False, end_cursor=end_cursor, count=1000)
            edge = following['data']['user'][edge_type]
            end_cursor = edge['page_info']['end_cursor']
            has_next_page = edge['page_info']['has_next_page']
            users = edge['edges']
            for user in users:
                self.ids[typeStr].append(user['node']['id'])

    def _apiGet(self, typeStr, id, extract=False, end_cursor=None, count=1000):
        if typeStr == 'followers':
            return self.api.user_followers(
                self.id, extract=False, end_cursor=end_cursor, count=1000)
        elif typeStr == 'following':
            return self.api.user_following(
                self.id, extract=False, end_cursor=end_cursor, count=1000)

    def start(self):
        self._isRunning = True
        self.get_api()
        self._get('following')
        self.follow()

    def stop(self):
        self._isRunning = False

    def get_api(self):
        try:
            self.api = self.client(
                auto_patch=True, authenticate=True,
                username=self.login, password=self.password)
            self.id = self.api.authenticated_user_id
            self.api_end.emit("Успешный вход в Инстаграмм")
        except ClientLoginError:
            self.end.emit("Неверный логин/пароль")
            return
        except (HTTPError, ClientError):
            self.end.emit("Слишком много запросов, придется подождать")
            return

    def _follow_subs_by_username(self, username):
        max_id = None
        has_next_page = 1
        while(has_next_page):
            user = self.api.user_info2(username)
            followers = self.api.user_followers(
                user['id'], max_id=max_id, count=1000)
            if(not len(followers)):
                return
            max_id = followers[len(followers) - 1]['id']
            has_next_page = len(followers)

            for follower in followers:
                if self._is_viable(follower):
                    self.api.friendships_create(follower['id'])
                    self.mid.emit(
                        "Подписался на " + follower['username'] + "\nПолное имя: " + follower['full_name'])
                    self._sleep()
        self.end.emit('Подписка закончена')  # TAA SHAA

    def _follow_subs_by_hashtag(self, hashtag):
        max_id = None
        has_next_page = True
        while(has_next_page):
            res = self.api.tag_feed(hashtag, max_id=max_id)
            media = res['tag']['media']
            has_next_page = media['page_info']['has_next_page']
            max_id = media['page_info']['end_cursor']
            items = media['nodes']
            for item in items:
                users_max_id = 0
                users_has_next_page = 1
                user_id = item['owner']['id']
                while(users_has_next_page):
                    followers = self.api.user_followers(
                        user_id, max_id=users_max_id, count=1000)
                    for follower in followers:
                        if self._is_viable(follower):
                            self.api.friendships_create(follower['id'])
                            self.mid.emit(
                                "Подписался на " + follower['username'] + "Полное имя: " + follower['full_name'])
                            self._sleep()
        self.end.emit('Подписка закончена')

    def _is_viable(self, follower):
        return (follower['id'] not in self.ignore_list and follower['id'] not in self.ids['followers'])

    def _follow_by_hashtag(self, hashtag):
        max_id = None
        has_next_page = True
        while(has_next_page):
            res = self.api.tag_feed(hashtag, max_id=max_id)
            media = res['tag']['media']
            has_next_page = media['page_info']['has_next_page']
            max_id = media['page_info']['end_cursor']
            items = media['nodes']
            for item in items:
                follower = item['owner']['id']
                self.api.friendships_create(follower)
                self.mid.emit(
                    "Подписался на " + follower)
                self._sleep()
        self.end.emit("Подписка закончена")
