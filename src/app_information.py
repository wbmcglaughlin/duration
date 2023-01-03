import os
import sys
from os import path, environ
from appdirs import *

DEBUG_MODE = False
APP_NAME = 'durations'
DURATIONS_FOLDER = './data/'
ARCHIVE_FOLDER = './archived/'
DEBUG_DURATIONS = './durations'


def get_app_path():
    if DEBUG_MODE:
        return DEBUG_DURATIONS

    return user_data_dir(APP_NAME, 'duration_app')


def get_app_data_path():
    return path.join(get_app_path(), DURATIONS_FOLDER)


def get_app_archive_path():
    return path.join(get_app_path(), ARCHIVE_FOLDER)


def get_duration_node_list():
    return [ele.removesuffix('.csv') for ele in list(os.listdir(get_app_data_path()))]
