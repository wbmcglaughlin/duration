#!/usr/bin/env python
from datetime import datetime
import os
import pandas as pd
import PySimpleGUI as sg
import sys
from os import path, environ

DEBUG_MODE = True

ALPHA = 0.7
THEME = 'black'
UPDATE_FREQUENCY_MILLISECONDS = 20 * 1000

BAR_COLORS = ('#23a0a0', '#56d856', '#be45be', '#5681d8', '#d34545', '#BE7C29')

APP_NAME = 'durations'
DURATION_COLUMNS = ['start', 'end', 'minutes']
DURATIONS_FOLDER = './data/'
DEBUG_DURATIONS = './durations'

def get_app_path():
    if DEBUG_MODE:
        return DEBUG_DURATIONS
    if sys.platform == 'win32':
        return path.join(environ['APPDATA'], APP_NAME)

def get_app_data_path():
    if sys.platform == 'win32':
        return path.join(get_app_path(), DURATIONS_FOLDER)

def create_new_duration_node(window, duration_node_name):
    pd.DataFrame(columns=DURATION_COLUMNS).to_csv(get_app_data_path() + duration_node_name + '.csv', index=False)

    window['-DATA_TYPE-'].update(value=duration_node_name + '.csv', values=list(os.listdir(get_app_data_path())))

def add_new_duration_entry(duration_node_name, start_time, end_time, seconds):
    df = pd.read_csv(get_app_data_path() + duration_node_name)
    df.loc[len(df)] = [start_time, end_time, seconds]

    df.to_csv(get_app_data_path() + duration_node_name, index=False)

def update_window(window):
    try:
        start_time = datetime.strptime(window['-START_TIME-'].get(), "%Y-%m-%d %H:%M:%S")
        time_now = datetime.now()
        elapsed_time = time_now - start_time

        duration_percent = elapsed_time.total_seconds() / 60 / 60 * 100
        if DEBUG_MODE:
            duration_percent *= 200

        window['-PROG-'].update(int(duration_percent))
        window['-ELAPSED_TIME-'].update(f'{elapsed_time.total_seconds() / 60:.2f}')

    except ValueError as e:
        pass


def main():
    sg.theme(THEME)

    # --------------- Get Duration Nodes -------------- #
    duration_nodes_list = os.listdir(get_app_data_path())

    # ----------------  Create Layout  ---------------- #
    layout = [[sg.Text('Duration', font='Any 16')]]

    layout += [[
        sg.Text('Add Duration:'),
        sg.InputText(size=(30, 1), key='-ADD_TYPE-'),
        sg.Text('Add', enable_events=True, key='ADD')
        ]]

    layout += [[
         sg.Text('Selected Node:'),
         sg.Combo(list(duration_nodes_list), size=(30, 1), key='-DATA_TYPE-'),
         sg.Text('Start', enable_events=True, key='START'),
         sg.Text('End', enable_events=True, key='END')
         ]]

    bar_color = sg.theme_progress_bar_color()
    this_color = BAR_COLORS[1 % len(BAR_COLORS)]

    layout += [[sg.Text("Duration", size=(5, 1), key='-NAME-'),
                sg.ProgressBar(100, 'h', size=(10, 15), key='-PROG-',
                               bar_color=(this_color, bar_color[1])),
                sg.Text("", size=(20, 1), key='-START_TIME-'),
                sg.Text("", size=(20, 1), key='-ELAPSED_TIME-')]],

    layout += [[sg.Text('Refresh', font='Any 8', key='-REFRESH-', enable_events=True),
                sg.Text('❎', enable_events=True, key='Exit Text')]]

    # ----------------  Create Window  ----------------
    window = sg.Window('Duration', layout, keep_on_top=True, grab_anywhere=True, no_titlebar=True,
                       alpha_channel=ALPHA, use_default_focus=False, finalize=True)

    update_window(window)  # sets the progress bars

    # ----------------  Event Loop  ----------------
    while True:
        event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
        if event == sg.WIN_CLOSED or event.startswith('Exit'):
            break
        elif event == 'ADD':
            create_new_duration_node(window, values['-ADD_TYPE-'])
        elif event == 'START':
            if window['-START_TIME-'].get() == "":
                window['-START_TIME-'].update(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        elif event == 'END':
            add_new_duration_entry(
                values['-DATA_TYPE-'],
                window['-START_TIME-'].get(),
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                window['-ELAPSED_TIME-'].get())

            window['-START_TIME-'].update("")
            window['-ELAPSED_TIME-'].update("")
            window['-PROG-'].update(int(0))

        update_window(window)


if __name__ == "__main__":
    if not os.path.exists(get_app_path()):
        os.mkdir(get_app_path())

    if not os.path.exists(get_app_data_path()):
        os.mkdir(get_app_data_path())

    main()
