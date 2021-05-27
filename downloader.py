from archiveOrgDownloader import ArchiveDownloader
from eapDownloader import EapDownloader
from os import link, read
from util import read_txt_file
from urllib.parse import urlsplit
from constants import *
import logging
import threading


def download_concurrently(each_link,logger,save_dir):
    logger.info(f"Downloading from : {each_link}")
    link_attr = urlsplit(each_link)
    if link_attr.netloc == ARCHIVE:
        down_inst = ArchiveDownloader(each_link,logger,save_dir)
    elif link_attr.netloc == EAP_BL_UK:
        down_inst = EapDownloader(each_link,logger,save_dir)
    down_inst.download()

class Downloader:

    def __init__(self,text_file_path,folder_to_save,logger) -> None:
        self.path = text_file_path
        self.save_dir = folder_to_save
        self.logger = logger

    def download(self):
        links = read_txt_file(self.path)
        threads = []
        for each_link in links:
            logger = self.logger
            save_dir = self.save_dir
            thread = threading.Thread(target=download_concurrently, args=(each_link,logger,save_dir))
            threads.append(thread)
            thread.start()
        for index,thread in enumerate(threads):
            thread.join()
            

if __name__ == "__main__":
    dow = Downloader("links.txt","Journal",logging)
    dow.download()