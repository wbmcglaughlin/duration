#!/usr/bin/env python
import subprocess
from datetime import datetime
import os
import pandas as pd
import PySimpleGUI as sg

from src.app_information import get_app_data_path, get_app_path, DEBUG_MODE
from src.generate_layout import generate_layout

ALPHA = 0.7
THEME = 'black'
UPDATE_FREQUENCY_MILLISECONDS = 20 * 1000

DURATION_COLUMNS = ['start', 'end', 'minutes']

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

        duration_percent = elapsed_time.total_seconds() / 60 / window['-DURATION_TIME-'].get() * 100
        if DEBUG_MODE:
            duration_percent *= 200

        window['-PROG-'].update(int(duration_percent))
        window['-ELAPSED_TIME-'].update(f'{elapsed_time.total_seconds() / 60:.2f}')

    except ValueError as e:
        pass


def main():
    sg.theme(THEME)

    # ----------------  Create Layout  ---------------- #
    layout = generate_layout()

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
        elif event == '-DATA_FOLDER-':
            abs_path = os.path.abspath(get_app_path())
            os.startfile(abs_path)

        update_window(window)


if __name__ == "__main__":
    if not os.path.exists(get_app_path()):
        os.mkdir(get_app_path())

    if not os.path.exists(get_app_data_path()):
        os.mkdir(get_app_data_path())

    main()
