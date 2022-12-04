from datetime import datetime

import pandas as pd
import os

from src.app_information import get_app_data_path, get_app_archive_path


def get_today_duration():
    duration_nodes_list = os.listdir(get_app_data_path())

    today_date = datetime.now().strftime("%Y-%m-%d")

    time = 0

    for duration_node in duration_nodes_list:
        df = pd.read_csv(get_app_data_path() + duration_node)

        today = df[df['start'].str.contains(today_date)]

        time += sum(today['minutes'])

    return time

def get_today_project_duration(duration_node):
    today_date = datetime.now().strftime("%Y-%m-%d")

    time = 0

    df = pd.read_csv(get_app_data_path() + duration_node)

    today = df[df['start'].str.contains(today_date)]

    time += sum(today['minutes'])

    return time

def get_total_project_time(duration_node, is_archived=True):
    time = 0

    if not is_archived:
        df = pd.read_csv(get_app_data_path() + duration_node)
    else:
        df = pd.read_csv(get_app_archive_path() + duration_node)

    time += sum(df['minutes'])

    return time
