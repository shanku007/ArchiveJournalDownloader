from tkinter import Scrollbar
import PySimpleGUI as sg
from driver import download
import os
import logging
import tempfile

buffer = ''

class Handler(logging.StreamHandler):

    def __init__(self,window):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer
        record = f'{record.name}: [{record.levelname}]: {record.message or "No message"}'
        buffer = f'{buffer}\n{record}'.strip()
        window['log'].update(value=buffer)

def create_logger(window):
    tmp = "download_log.txt"
    logger = logging
    logger.basicConfig(
        level=logging.DEBUG,
        format='%(name)s, %(asctime)s, [%(levelname)s], %(message)s',
        filename=tmp,
        filemode='w')
    ch = Handler(window)
    ch.setLevel(logging.INFO)
    logging.getLogger('').addHandler(ch)
    return logger

sg.theme("DarkTeal2")
layout = [[sg.T("")],
            [sg.Text("Choose a folder to save: "),
            sg.Input(key="DOWNLOAD-FOLDER-IN", change_submits=True),
            sg.FolderBrowse(key="DOWNLOAD-FOLDER-BUTTON")],
            [sg.Text("Select the text file with links"),
            sg.Input(key="Text-FILE-IN", change_submits=True),
            sg.FileBrowse(key="Text-FILE-BUTTON")],
            [sg.Button("Submit")],
            [sg.Output(size=(500, 100), key='log')]]

# Building Window
window = sg.Window('Old Archive Downloads', layout, size=(600, 500))
logger = create_logger(window)

def create_GUI():
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Submit":
            window['Submit'].update(disabled=True)
            if os.path.exists(values["Text-FILE-IN"]) and os.path.exists(values["DOWNLOAD-FOLDER-BUTTON"]):
                logger.info("Starting to Downloading files")
                download(
                    values["Text-FILE-IN"], values["DOWNLOAD-FOLDER-BUTTON"], logger)
            else:
                logger.info(
                    "Please give the folder to save and the text file with links")
                window['Submit'].update(disabled=False)
            logger.info("Please see the download_log.txt in the current folder to see a complete log")

    window.close()


if __name__ == "__main__":
    create_GUI()
