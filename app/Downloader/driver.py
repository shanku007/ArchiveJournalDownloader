from app.Downloader.archiveOrgDownloader import ArchiveDownloader
from app.Downloader.eapDownloader import EapDownloader
from app.Commons.util import read_txt_file
from urllib.parse import urlsplit
from app.Commons.constants import *
import logging
import asyncio
from functools import partial
from concurrent.futures import ThreadPoolExecutor


def download_concurrently(save_dir,each_link):
    logging.info(f"Downloading from : {each_link}")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    link_attr = urlsplit(each_link)
    if link_attr.netloc == ARCHIVE:
        down_inst = ArchiveDownloader(each_link,save_dir)
    elif link_attr.netloc == EAP_BL_UK:
        down_inst = EapDownloader(each_link,save_dir)
    loop.run_until_complete(down_inst.download())
    logging.info(f"Downloaded {each_link}")


def download(text_file_path,folder_to_save):
    links = read_txt_file(text_file_path)
    # for each_link in links:
        # thread = threading.Thread(target=download_concurrently, args=(each_link,logger,folder_to_save))
        # thread.start()
        # download_concurrently(each_link,logger,folder_to_save)
    with ThreadPoolExecutor(max_workers=4) as executor:

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