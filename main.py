#!/usr/bin/env python
import os
import pandas as pd
import PySimpleGUI as sg

"""
    Desktop "Rainmeter" style widget - Drive usage
    Requires: psutil
    Shows a bar graph of space used for each drive partician that psutil finds
"""

ALPHA = 0.7
THEME = 'black'
UPDATE_FREQUENCY_MILLISECONDS = 20 * 1000

BAR_COLORS = ('#23a0a0', '#56d856', '#be45be', '#5681d8', '#d34545', '#BE7C29')

DURATIONS_FOLDER = './durations/'

def create_new_duration_node(duration_node_name):
    pd.DataFrame(columns=['start', 'end']).to_csv(DURATIONS_FOLDER + duration_node_name + '.csv', index=False)

def update_window(window):
    pass


def main():
    sg.theme(THEME)

    # --------------- Get Duration Nodes -------------- #
    duration_nodes_list = os.listdir('./durations')

    # ----------------  Create Layout  ---------------- #

    layout = [[sg.Text('Duration', font='Any 16')]]
    layout += [[sg.Text('Add Duration:'),
               sg.InputText(key='-ADD_TYPE-'),
               sg.Text('Add', enable_events=True, key='ADD')
                ]]
    layout += [
        [sg.Text('Selected Node:'),
         sg.Combo(list(duration_nodes_list), size=(20, 1), key='-DATA_TYPE-'),
         sg.Text('Start', enable_events=True, key='START')]]

    bar_color = sg.theme_progress_bar_color()
    this_color = BAR_COLORS[1 % len(BAR_COLORS)]

    layout += [[sg.Text("Duration", size=(5, 1), key='-NAME-'),
                sg.ProgressBar(100, 'h', size=(10, 15), key='-PROG-',
                               bar_color=(this_color, bar_color[1]))]],

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
            create_new_duration_node(values['-ADD_TYPE-'])
        elif event == 'START':
            print(values['-DATA_TYPE-'])

        update_window(window)


if __name__ == "__main__":
    main()
