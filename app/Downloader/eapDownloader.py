from app.Commons.util import (
    create_base_link_for_eap,
    save_file,
    create_folder,
    convert_to_pdf
)
import os
from app.Downloader.downloader import Downloader
from app.Commons.request import makeParallelGet
import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
import requests



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


    async def download(self):
        get_url,get_basepath = create_base_link_for_eap(self.url)
        folder_to_store = os.path.join(self.save_dir,get_basepath())
        create_folder(os.path.join(folder_to_store,"images"))
        files_already_downloaded = os.listdir(os.path.join(folder_to_store,"images"))
        try:
            with ThreadPoolExecutor(max_workers=4) as executor:
                with requests.Session() as session:
                # Set any session parameters here before calling `fetch`

                # Initialize the event loop        
                    loop = asyncio.get_event_loop()
                    tasks = [
                    loop.run_in_executor(
                        executor,
                        makeParallelGet,
                        *(session, get_url(i)) # Allows us to pass in multiple arguments to `fetch`
                    )
                    for i in range(1,1300) if f"image_{i}.jpg" not in files_already_downloaded
                ]

                for index,response in enumerate(await asyncio.gather(*tasks)):
                    self.logger.info(f"Downloading {index}th file of {get_basepath()}")
                    file_path_to_save = os.path.join(folder_to_store,"images",f"image_{index}.jpg")
                    if response.status_code != 200:
                        break
                    else:
                        content = response.content
                        save_file(file_path_to_save,content)
            images_dir = os.path.join(folder_to_store,"images")
            path_to_pdf = f"{folder_to_store}/{get_basepath()}.pdf"
            convert_to_pdf(images_dir,path_to_pdf,self.logger)

        except Exception as e:
            print(e)
            self.logger.error(f"Error downloading files  of {get_basepath()}")
            self.logger.warning(f"I suggest you to rerun the program for {self.url}")
            

        

if __name__ == "__main__":
    downloader = EapDownloader("https://eap.bl.uk/archive-file/EAP781-1-5-103")
    downloader.convert_to_pdf("Journal/EAP781_1_5_95/images","test.pdf")



