from datetime import datetime
import os
import pandas as pd
import PySimpleGUI as sg

from src.app_information import get_app_data_path, get_app_path, DEBUG_MODE, get_app_archive_path
from src.duration_handler import add_new_duration_entry, create_new_duration_node, archive_duration
from src.user_data import get_today_duration, get_today_project_duration, get_total_project_time

UPDATE_FREQUENCY_MILLISECONDS = 20 * 1000

def run_app(window):
    while True:
        event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)

        if event == sg.WIN_CLOSED or event.startswith('Exit'):
            # If program is closed.

            if window['-START_TIME-'].get() != "":
                send_to_duration_entry(window, values)

            break

        elif event == 'ADD':
            # If new duration node is added.
            create_new_duration_node(window, values['-ADD_TYPE-'])

        elif event == 'START':
            # If start of new session.
            if window['-START_TIME-'].get() == "":
                window['-START_TIME-'].update(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            current = values['-DATA_TYPE-']
            if current != "":
                window['-PROJECT_TIME-'].update(get_total_project_time(current))

        elif event == 'END':
            # If end of session.
            if window['-START_TIME-'].get() != "":
                send_to_duration_entry(window, values)

            update_values_on_reset(window, values)

        elif event == '-DATA_FOLDER-':
            # If open data text is clicked.
            abs_path = os.path.abspath(get_app_path())
            os.startfile(abs_path)

        elif event == '-ARCHIVE_DURATION-':
            # If end of session.
            if window['-START_TIME-'].get() != "":
                send_to_duration_entry(window, values)
            if values['-DATA_TYPE-'] != "":
                archive_duration(window, values)

        elif event == '-CANCEL-':
            update_values_on_reset(window, values)

        update_window(window)

def update_window(window):
    try:
        start_time = datetime.strptime(window['-START_TIME-'].get(), "%Y-%m-%d %H:%M:%S")
        time_now = datetime.now()
        elapsed_time = time_now - start_time

        duration_percent = elapsed_time.total_seconds() / 60 / window['-DURATION_TIME-'].get() * 100
        if DEBUG_MODE:
            duration_percent *= 10

        window['-PROG-'].update(int(duration_percent))
        window['-ELAPSED_TIME-'].update(f'{elapsed_time.total_seconds() / 60:.2f}')

    except ValueError as e:
        pass

def update_values_on_reset(window, values):
    window['-START_TIME-'].update("")
    window['-ELAPSED_TIME-'].update("")
    window['-PROG-'].update(int(0))
    window['-TIME_TODAY-'].update(f'{get_today_duration():.2f}')

    current = values['-DATA_TYPE-']
    if current != "":
        window['-PROJECT_TIME_TODAY-'].update(f"{get_today_project_duration(values['-DATA_TYPE-']):.2f}")
        window['-PROJECT_TIME-'].update(get_total_project_time(current))

def send_to_duration_entry(window, values):
    if values['-DATA_TYPE-'] != "":
        add_new_duration_entry(
            values['-DATA_TYPE-'],
            window['-START_TIME-'].get(),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            window['-ELAPSED_TIME-'].get())
