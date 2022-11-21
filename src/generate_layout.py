import os

import PySimpleGUI as sg

from src.app_information import get_app_data_path

BAR_COLORS = ('#23a0a0', '#56d856', '#be45be', '#5681d8', '#d34545', '#BE7C29')

def generate_layout():
    # --------------- Get Duration Nodes -------------- #
    duration_nodes_list = os.listdir(get_app_data_path())

    layout = [[sg.Text('Duration', font='Any 16')]]

    layout += [[
        sg.Text('New:'),
        sg.InputText(size=(20, 1), key='-ADD_TYPE-'),
        sg.Text('Add', enable_events=True, key='ADD'),
        sg.Combo(list([15, 30, 45, 60]), size=(5, 1), key='-DURATION_TIME-')
    ]]

    layout += [[
        sg.Text('Selected:'),
        sg.Combo(list(duration_nodes_list), size=(20, 1), key='-DATA_TYPE-'),
        sg.Text('Start', enable_events=True, key='START'),
        sg.Text('End', enable_events=True, key='END')
    ]]

    bar_color = sg.theme_progress_bar_color()
    this_color = BAR_COLORS[1 % len(BAR_COLORS)]

    layout += [[sg.Text("Duration: ", key='-NAME-'),
                sg.ProgressBar(100, 'h', size=(10, 18), key='-PROG-',
                               bar_color=(this_color, bar_color[1])),
                sg.Text("", size=(20, 1), key='-START_TIME-')]],

    layout += [[sg.Text('Refresh', font='Any 8', key='-REFRESH-', enable_events=True),
                sg.Text('❎', enable_events=True, key='Exit Text'),
                sg.Text("", size=(20, 1), key='-ELAPSED_TIME-'),
                sg.Text("Open Data", key='-DATA_FOLDER-', enable_events=True, justification='right')]]

    return layout

def main_tab():
    pass

def add_tab():
    pass

def settings_tab():
    pass