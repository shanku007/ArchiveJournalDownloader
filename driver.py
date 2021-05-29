from archiveOrgDownloader import ArchiveDownloader
from eapDownloader import EapDownloader
from os import link, read
from util import read_txt_file
from urllib.parse import urlsplit
from constants import *
import logging
import threading
from functools import partial
from time import time
from concurrent.futures import ThreadPoolExecutor


def download_concurrently(save_dir,each_link):
    logging.info(f"Downloading from : {each_link}")
    link_attr = urlsplit(each_link)
    if link_attr.netloc == ARCHIVE:
        down_inst = ArchiveDownloader(each_link,save_dir)
    elif link_attr.netloc == EAP_BL_UK:
        down_inst = EapDownloader(each_link,save_dir)
    down_inst.download()


def download(text_file_path,folder_to_save):
    links = read_txt_file(text_file_path)
    # for each_link in links:
        # thread = threading.Thread(target=download_concurrently, args=(each_link,logger,folder_to_save))
        # thread.start()
        # download_concurrently(each_link,logger,folder_to_save)
    with ThreadPoolExecutor() as executor:

        # Create a new partially applied function that stores the directory
        # argument.
        # 
        # This allows the download_link function that normally takes two
        # arguments to work with the map function that expects a function of a
        # single argument.
        fn = partial(download_concurrently, folder_to_save)

        # Executes fn concurrently using threads on the links iterable. The
        # timeout is for the entire process, not a single call, so downloading
        # all images must complete within 30 seconds.
        executor.map(fn, links)


if __name__ == "__main__":
    download("links.txt","Journal")