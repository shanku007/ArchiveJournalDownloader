from app.Commons.util import (
    create_base_link_for_eap,
    save_file,
    create_folder,
    convert_to_pdf
)
import os
from app.Downloader.downloader import Downloader
import logging
from bs4 import BeautifulSoup
from app.Commons.request import makeGet
import re


class EapDownloader(Downloader):

    def __init__(
        self,
        url,
        save_dir=os.path.dirname(os.path.realpath(__file__))
    ) -> None:
        self.url = url
        self.save_dir = save_dir
        self.logger = logging
        super().__init__()

    def get_number_of_files(self):
        soup = BeautifulSoup(makeGet(self.url).content, 'html.parser')
        text = soup.find(
            'a', {"class": ["action-button", "open-uv"]}).find(
                'span', {"class": "action-text"}).text
        return int(re.search(r'\((.*?)\)',text).group(1))

    async def download(self):
        get_url, get_basepath = create_base_link_for_eap(self.url)
        folder_to_store = os.path.join(self.save_dir, get_basepath())
        create_folder(os.path.join(folder_to_store, "images"))
        files_already_downloaded = os.listdir(
            os.path.join(folder_to_store, "images"))
        number_of_files = self.get_number_of_files()
        urls = [get_url(i) for i in range(
                    1, number_of_files+1) if f"image_{i}.jpg" not in files_already_downloaded]
        try:
            for url in urls:
                try:
                    index = int(url.split('/')[5].split('.')[0])
                    print(f"Downloading {index}th file of {get_basepath()}")
                    file_path_to_save = os.path.join(
                        folder_to_store, "images", f"image_{index+1}.jpg")
                    response = makeGet(url)
                except Exception as e:
                    self.logger.info(f"Error downloading {index}th image of {get_basepath()}")
                    continue
                else:
                    if response.status_code != 200:
                        continue
                    else:
                        content = response.content
                        save_file(file_path_to_save, content)
                
            images_dir = os.path.join(folder_to_store, "images")
            path_to_pdf = f"{folder_to_store}/{get_basepath()}.pdf"
            convert_to_pdf(images_dir, path_to_pdf, self.logger)

        except Exception as e:
            print(e)
            self.logger.error(f"Error downloading files  of {get_basepath()}")
            self.logger.warning(
                f"I suggest you to rerun the program for {self.url}")

if __name__ == "__main__":
    downloader = EapDownloader("https://eap.bl.uk/archive-file/EAP781-1-5-103",
                               "/Users/shankar.jha/Practice/webScrapping/archiveDownloader/Journal")
    downloader.download()
