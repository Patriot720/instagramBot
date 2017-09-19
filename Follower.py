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

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.id = api.authenticated_user_id
        self._create_ignore_list()
        self.functions = [
            self._follow_subs_by_username,
            self._follow_subs_by_hashtag,
            self._follow_by_hashtag,
            self.removeFollowing
        ]
        self._isRunning = True
        self.followers = [] # TODO change to sublsidfjlManger

    def _create_ignore_list(self):
        if(os.path.isfile("ignoreList.txt")):
            ignore = open("ignoreList.txt", 'r')
            self.ignore_list = ignore.read().splitlines()
            ignore.close()
        else:
            self.ignore_list = []

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
        followings = self.api.get('following', self.id)
        self.mid.emit('Скачал все подписки')
        followers = self.api.get('followers', self.id)
        followers = []
        self.mid.emit('Скачал всех подписчиков')
        for user in followings:
            if(user not in followers):
                self.api.friendships_destroy(user)
                self.mid.emit("Удалил" + str(user))
                self._sleep()
        self.end.emit("Завершено")

    def setSleepFunction(self, func):
        self._sleep = func

    def _sleep(self):
        for i in range(SLEEP_TIME_MODULE):
            if(not self._isRunning):
                self.end.emit(STANDART_STOP_MESSAGE)
                return
            time.sleep(SLEEP_TIME / SLEEP_TIME_MODULE)

    def start(self):
        self._isRunning = True
        self._get('following')
        self.follow()

    def stop(self):
        self._isRunning = False

    def _follow_subs_by_username(self, username):
        max_id = None
        has_next_page = 1
        user_id = self.api.get_user_id(username)
        followers = self.api.get("followers", user_id)
        for follower in followers:
            if self._is_viable(follower):
                self.api.friendships_create(follower)
                self.mid.emit(
                    "Подписался на " + str(follower))
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

    def _is_viable(self, user_id):
        return (user_id not in self.ignore_list and user_id not in self.followers)

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
