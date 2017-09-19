# -*- coding: utf8 -*-
from PyQt5.QtCore import QObject, pyqtSignal
import os.path
import time
from urllib.error import (HTTPError)
from instagram_web_api import Client, ClientCompatPatch, ClientError, ClientLoginError


class Follower(QObject):
    api_end = pyqtSignal(str)
    end = pyqtSignal(str)
    mid = pyqtSignal(str)
    SUBS_BY_HASTAG_COUNT = 1
    SUCCESS_END_MESSAGE = "Успешно завершено"
    HTTPERROR_MESSAGE = "Слишком много запросов, придется подождать"
    VALUEERROR_MESSAGE = "Неверный ник/тег"
    CLIENTERROR_MESSAGE = "Instagram блочит или неверный ник/тег"
    SLEEP_TIME = 60
    SLEEP_TIME_MODULE = 60

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.id = api.authenticated_user_id
        self._create_ignore_list()
        self.functions = [
            self._follow_subs_by_username,
            self._follow_subs_by_hashtag,
            self._follow_by_hashtag,
            self._remove_following
        ]
        self._isRunning = True
        self.followers = self.api.get("followers", self.id)

    def start(self):
        self._isRunning = True
        self._follow()

    def stop(self):
        self._isRunning = False

    def set_sleep_function(self, func):
        self._sleep = func

    def _remove_following(self, name):
        followings = self.api.get('following', self.id)
        self.mid.emit('Скачал все подписки')
        followers = self.api.get('followers', self.id)
        self.mid.emit('Скачал всех подписчиков')
        for user in followings:
            if(user not in followers):
                self.api.friendships_destroy(user)
                self.mid.emit("Удалил" + str(user))
                self._sleep()
        self.end.emit(self.SUCCESS_END_MESSAGE)

    def _create_ignore_list(self):
        if(os.path.isfile("ignoreList.txt")):
            ignore = open("ignoreList.txt", 'r')
            self.ignore_list = ignore.read().splitlines()
            ignore.close()
        else:
            self.ignore_list = []

    def _follow(self):
        try:
            self.functions[self.index](self.text)
        except ClientError as e:
            self.end.emit(self.CLIENTERROR_MESSAGE)
        except ValueError:
            self.end.emit(self.VALUEERROR_MESSAGE)
        except HTTPError:
            self.end.emit(self.HTTPERROR_MESSAGE)

    def _sleep(self):
        for i in range(self.SLEEP_TIME_MODULE):
            if(not self._isRunning):
                self.end.emit(self.SUCCESS_END_MESSAGE)
                return
            time.sleep(self.SLEEP_TIME / self.SLEEP_TIME_MODULE)

    def _follow_subs_by_username(self, username):
        user_id = self.api.get_user_id(username)
        followers = self.api.get("followers", user_id)
        self._subscribe_on_all(followers)
        self.end.emit(self.SUCCESS_END_MESSAGE)  # TAA SHAA

    def _follow_subs_by_hashtag(self, hashtag):
        user_ids = self.api.get_user_ids_from_tag_feed(
            hashtag, count=self.SUBS_BY_HASTAG_COUNT)
        for user_id in user_ids:
            followers = self.api.get("followers", user_id)
            self._subscribe_on_all(followers)
        self.end.emit('Подписка закончена')

    def _is_viable(self, user_id):
        return (user_id not in self.ignore_list and user_id not in self.followers)

    def _subscribe_on_all(self, followers):
        for follower in followers:
            if self._is_viable(follower):
                self._subscribe(follower)
                self._sleep()

    def _subscribe(self, user_id):
        self.api.friendships_create(user_id)
        self.mid.emit("Подписался на " + str(user_id))

    def _follow_by_hashtag(self, hashtag):
        end_cursor = None
        has_next_page = True
        followers = self.api.get_user_ids_from_tag_feed(
            hashtag, end_cursor=end_cursor)
        self._subscribe_on_all(followers)
        self.end.emit(self.SUCCESS_END_MESSAGE)
