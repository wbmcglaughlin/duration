import sys
from os import path, environ

DEBUG_MODE = True
APP_NAME = 'durations'

DURATIONS_FOLDER = './data/'
ARCHIVE_FOLDER = './archived/'
DEBUG_DURATIONS = './durations'


def get_app_path():
    if DEBUG_MODE:
        return DEBUG_DURATIONS
    if sys.platform == 'win32':
        return path.join(environ['APPDATA'], APP_NAME)


def get_app_data_path():
    if sys.platform == 'win32':
        return path.join(get_app_path(), DURATIONS_FOLDER)


def get_app_archive_path():
    if sys.platform == 'win32':
        return path.join(get_app_path(), ARCHIVE_FOLDER)