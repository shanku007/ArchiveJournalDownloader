from tkinter import Scrollbar
import PySimpleGUI as sg
from Downloader.driver import download
import os
import logging
import tempfile
import threading

buffer = ''

class Handler(logging.StreamHandler):

    def __init__(self,window):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        global buffer
        record = f'{record.name}: [{record.levelname}]: {record.message or "No message"}'
        record = f'\n{record}'.strip()
        window['log'].update(value=record,append=True)


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

def TextLabel(text): return sg.Text(text+':', justification='l', size=(30,1))

sg.theme("BluePurple")
layout = [[sg.T("")],
            [TextLabel("Choose a folder to save: "),
            sg.Input(key="DOWNLOAD-FOLDER-IN", change_submits=True),
            sg.FolderBrowse(key="DOWNLOAD-FOLDER-BUTTON")],
            [TextLabel("Select the text file with links"),
            sg.Input(key="Text-FILE-IN", change_submits=True),
            sg.FileBrowse(key="Text-FILE-BUTTON")],
            [sg.Button("Download files",
            size=(15,2),
            )],
            [TextLabel("Made with ❤️ Shankar Jha")],
            [sg.Multiline(size=(500, 100), key='log')]]

# Building Window
window = sg.Window('Old Archive Downloads', layout, size=(600, 500))
logger = create_logger(window)

def create_GUI():
    while True:
        event, values = window.read(timeout=400)
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Download files":
            window['Download files'].update(disabled=True)
            window['DOWNLOAD-FOLDER-BUTTON'].update(disabled=True)
            window['Text-FILE-BUTTON'].update(disabled=True)
            if os.path.exists(values["Text-FILE-IN"]) and os.path.exists(values["DOWNLOAD-FOLDER-IN"]):
                logger.info("Starting to Downloading files")
                threading.Thread(target=download, args=(values["Text-FILE-IN"], values["DOWNLOAD-FOLDER-BUTTON"]), daemon=True).start()
            else:
                logger.info(
                    "Please give the folder to save and the text file with links")
                window['Download files'].update(disabled=False)
            logger.info("Please see the download_log.txt in the current folder to see a complete log")

    window.close()


if __name__ == "__main__":
    create_GUI()
