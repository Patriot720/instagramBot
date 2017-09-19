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
            self.follow_subs_by_username,
            self.follow_subs_by_hashtag,
            self.follow_by_hashtag,
            self.removeFollowing
        ]
        self._isRunning = True
        self.following_ids = []
        self.followers_ids = []

    def follow(self):
        try:
            self.functions[self.index](self.text)
        except ClientError as e:
            print("ERR", e)
            self.end.emit("Неверный ник/тег")
        except ValueError:
            self.end.emit("Неверный ник/тег")
        except HTTPError:
            self.end.emit("Слишком много запросов, придется подождать")

    def removeFollowing(self, name):
        self.getFollowing()
        self.mid.emit('Скачал все подписки')
        self._getFollowers()
        self.mid.emit('Скачал всех подписчиков')
        for user in self.following_ids:
            if(user not in self.followers_ids):
                self.api.friendships_destroy(user)
                self.mid.emit("Удалил" + user)
                print(user)
                for i in range(SLEEP_TIME_MODULE):
                    if(not self._isRunning):
                        self.end.emit(STANDART_STOP_MESSAGE)
                        return
                    time.sleep(SLEEP_TIME / SLEEP_TIME_MODULE)
        self.end.emit("КОНЧИЛ")

    def _getFollowers(self):
        has_next_page = True
        end_cursor = None
        while(has_next_page):
            followers = self.api.user_followers(
                self.id,extract=False, end_cursor=end_cursor, count=1000)
            end_cursor = followers['data']['user']['edge_followed_by']['page_info']['end_cursor']
            has_next_page = followers['data']['user']['edge_followed_by']['page_info']['has_next_page']
            follower_users = followers['data']['user']['edge_followed_by']['edges']
            for user in follower_users:
                self.followers_ids.append(user['node']['id'])

    def start(self):
        self._isRunning = True
        self.get_api()
        self.getFollowing()
        self.follow()

    def getFollowing(self):
        has_next_page = True
        end_cursor = None
        while(has_next_page):
            following = self.api.user_following(
                self.id, extract=False, end_cursor=end_cursor, count=1000)
            end_cursor = following['data']['user']['edge_follow']['page_info']['end_cursor']
            has_next_page = following['data']['user']['edge_follow']['page_info']['has_next_page']
            following_users = following['data']['user']['edge_follow']['edges']
            for user in following_users:
                self.following_ids.append(user['node']['id'])

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

    def follow_subs_by_username(self, username):
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
                if self.is_viable(follower):
                    self.api.friendships_create(follower['id'])
                    self.mid.emit(
                        "Подписался на " + follower['username'] + "\nПолное имя: " + follower['full_name'])
                    for i in range(SLEEP_TIME_MODULE):
                        if(not self._isRunning):
                            self.end.emit(STANDART_STOP_MESSAGE)
                            return
                        time.sleep(SLEEP_TIME / SLEEP_TIME_MODULE)
        self.end.emit('Подписка закончена')  # TAA SHAA

    def follow_subs_by_hashtag(self, hashtag):
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
                        if self.is_viable(follower):
                            self.api.friendships_create(follower['id'])
                            self.mid.emit(
                                "Подписался на " + follower['username'] + "Полное имя: " + follower['full_name'])
                            for i in range(SLEEP_TIME_MODULE):
                                if(not self._isRunning):
                                    self.end.emit(STANDART_STOP_MESSAGE)
                                    return
                                time.sleep(SLEEP_TIME / SLEEP_TIME_MODULE)
        self.end.emit('Подписка закончена')

    def is_viable(self, follower):
        return (follower['id'] not in self.ignore_list and follower['id'] not in self.following_ids)

    def follow_by_hashtag(self, hashtag):
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
                for i in range(SLEEP_TIME_MODULE):
                    if(not self._isRunning):
                        self.end.emit(STANDART_STOP_MESSAGE)
                        return
                    time.sleep(SLEEP_TIME / SLEEP_TIME_MODULE)
        self.end.emit("Подписка закончена")
