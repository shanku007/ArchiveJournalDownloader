from archiveOrgDownloader import ArchiveDownloader
from eapDownloader import EapDownloader
from os import link, read
from util import read_txt_file
from urllib.parse import urlsplit
from constants import *
import logging
import asyncio
from concurrent.futures.thread import ThreadPoolExecutor


def download_concurrently(each_link,logger,save_dir):
    logger.info(f"Downloading from : {each_link}")
    link_attr = urlsplit(each_link)
    if link_attr.netloc == ARCHIVE:
        down_inst = ArchiveDownloader(each_link,logger,save_dir)
    elif link_attr.netloc == EAP_BL_UK:
        down_inst = EapDownloader(each_link,logger,save_dir)
    down_inst.download()


async def download(text_file_path,folder_to_save,logger):
    loop = asyncio.get_running_loop()
    executor = ThreadPoolExecutor(max_workers=4)
    links = read_txt_file(text_file_path)
    futures = []
    for each_link in links:
        args = (each_link,logger,folder_to_save)
        futures.append(loop.run_in_executor(executor, download_concurrently, *args))
    # for each_link in links:
        # thread = threading.Thread(target=download_concurrently, args=(each_link,logger,folder_to_save))
        # threads.append(thread)
        # thread.start()
        # download_concurrently(each_link,logger,folder_to_save)
    
    results = await asyncio.gather(*futures)



if __name__ == "__main__":
    asyncio.run(download("links.txt","Journal",logging))