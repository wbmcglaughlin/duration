from datetime import datetime

import pandas as pd
import os

from src.app_information import get_app_data_path


def get_today_duration():
    duration_nodes_list = os.listdir(get_app_data_path())

    today_date = datetime.now().strftime("%Y-%m-%d")

    time = 0

    for duration_node in duration_nodes_list:
        df = pd.read_csv(get_app_data_path() + duration_node)

        today = df[df['start'].str.contains(today_date)]

        time += sum(today['minutes'])

    return time
