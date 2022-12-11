#!/usr/bin/env python
import os
import PySimpleGUI as sg

from src.app_information import get_app_data_path, get_app_path, get_app_archive_path
from src.app_loop import run_app, update_window
from src.generate_layout import generate_layout

ALPHA = 0.7
THEME = 'black'


def main():
    sg.theme(THEME)

    # ----------------  Create Layout  ---------------- #
    layout = generate_layout()

    # ----------------  Create Window  ---------------- #
    window = sg.Window('Duration', layout, keep_on_top=True, grab_anywhere=True, no_titlebar=True,
                       alpha_channel=ALPHA, use_default_focus=False, finalize=True)

    update_window(window)  # sets the progress bars

    run_app(window)


if __name__ == "__main__":
    if not os.path.exists(get_app_path()):
        os.mkdir(get_app_path())

    if not os.path.exists(get_app_data_path()):
        os.mkdir(get_app_data_path())

    if not os.path.exists(get_app_archive_path()):
        os.mkdir(get_app_archive_path())

    main()
