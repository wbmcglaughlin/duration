import os

import pandas as pd

from src.app_information import get_app_data_path, get_app_archive_path

DURATION_COLUMNS = ['start', 'end', 'minutes']

def create_new_duration_node(window, duration_node_name):
    pd.DataFrame(columns=DURATION_COLUMNS).to_csv(get_app_data_path() + duration_node_name + '.csv', index=False)

    window['-DATA_TYPE-'].update(value=duration_node_name + '.csv', values=list(os.listdir(get_app_data_path())))


def add_new_duration_entry(duration_node_name, start_time, end_time, seconds):
    df = pd.read_csv(get_app_data_path() + duration_node_name)
    df.loc[len(df)] = [start_time, end_time, seconds]

    df.to_csv(get_app_data_path() + duration_node_name, index=False)

def archive_duration(window, values):
    os.rename(get_app_data_path() + values['-DATA_TYPE-'], get_app_archive_path() + values['-DATA_TYPE-'])

    left_over_nodes = list(os.listdir(get_app_data_path()))
    if len(left_over_nodes) > 0:
        window['-DATA_TYPE-'].update(value=left_over_nodes[0], values=left_over_nodes)
    else:
        window['-DATA_TYPE-'].update(value='', values=left_over_nodes)

