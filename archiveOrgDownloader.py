from logging import log
import os
from posixpath import basename
from util import create_folder, find_pdf_link,save_file
from request import makeGet
from bs4 import BeautifulSoup

class ArchiveDownloader:

    def __init__(
        self,
        url,
        logger,
        save_dir=os.path.dirname(os.path.realpath(__file__)),
        ) -> None:
        self.url = url
        self.save_dir = save_dir
        self.logger = logger

    def crawl_for_links(self,url,div_class,fetch_name=False):
        soup = BeautifulSoup(makeGet(url).content, 'html.parser')
        div_with_links = soup.find_all('div',class_=div_class)
        links = []
        for each_item in div_with_links:
            data = {}
            next_link = each_item.find('a')['href']
            data["link"] = next_link
            if fetch_name:
                data["name"] = each_item.find('a').find('div',class_="ttl").text.strip()
            links.append(data)
        return links


    def download(self):
        links = self.crawl_for_links(self.url,'item-ttl',fetch_name=True)
        for each_link in links:
            basepath = f"{each_link['name']}"
            self.logger.info("Downloading",basepath)
            try:
                folder_to_save = os.path.join(self.save_dir,basepath)
                create_folder(folder_to_save)
                complete_link = f"https://archive.org{each_link['link']}"
                download_links = self.crawl_for_links(complete_link,"format-group")
                pdf_link = find_pdf_link(download_links)
                if not pdf_link:
                    self.logger.warning("No pdf link found Trying to download first link")
                    self.logger.warning("I suggest you to manually download this file from {complete_link}")
                    pdf_link = download_links[0]["link"]
                    file_path_to_save = os.path.join(folder_to_save,os.path.basename(pdf_link))
                else:
                    file_path_to_save = os.path.join(folder_to_save,os.path.basename(pdf_link))
                if os.path.exists(file_path_to_save):
                    continue
                response = makeGet(pdf_link)
                if response.status_code != 200:
                    continue
                else:
                    content = response.content
                    save_file(file_path_to_save,content)
            except Exception as err:
                self.logger.info(err)
                self.logger.error(f"Error downloading basepath")


if __name__ == "__main__":
  process = ArchiveDownloader("https://archive.org/search.php?query=Nagri+Pracharini+Patrika")
  process.download()

    




