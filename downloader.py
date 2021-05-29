from archiveOrgDownloader import ArchiveDownloader
from eapDownloader import EapDownloader
from os import link, read
from util import read_txt_file
from urllib.parse import urlsplit
from constants import *
import logging


class Downloader:

    def __init__(self,text_file_path,folder_to_save,logger) -> None:
        self.path = text_file_path
        self.save_dir = folder_to_save
        self.logger = logger

    def download(self):
        links = read_txt_file(self.path)

        for each_link in links:
            self.logger.info(f"Downloading from : {each_link}")
            link_attr = urlsplit(each_link)
            if link_attr.netloc == ARCHIVE:
                down_inst = ArchiveDownloader(each_link,self.logger,self.save_dir)
            elif link_attr.netloc == EAP_BL_UK:
                down_inst = EapDownloader(each_link,self.logger,self.save_dir)
            else:
                continue
            down_inst.download()


if __name__ == "__main__":
    dow = Downloader("links.txt","Journal",logging)
    dow.download()