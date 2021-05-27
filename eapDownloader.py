from util import (
    create_base_link_for_eap,
    save_file,
    create_folder,
    convert_to_pdf
)
import os
from request import makeGet



class EapDownloader:

    def __init__(
        self,
        url,
        logger,
        save_dir=os.path.dirname(os.path.realpath(__file__))
        ) -> None:
        self.url = url
        self.save_dir = save_dir
        self.logger = logger


    def download(self):
        get_url,get_basepath = create_base_link_for_eap(self.url)
        folder_to_store = os.path.join(self.save_dir,get_basepath())
        create_folder(os.path.join(folder_to_store,"images"))
        for i in range(1,100000):
            self.logger.info(f"Downloading {i}th file of {get_basepath()}")
            try:
                file_path_to_save = os.path.join(folder_to_store,"images",f"image_{i}.jpg")
                files_already_downloaded = os.listdir(os.path.join(folder_to_store,"images"))
                if os.path.basename(file_path_to_save) in files_already_downloaded:
                    continue
                response = makeGet(get_url(i))
                if response.status_code != 200:
                    break
                else:
                    content = response.content
                    save_file(file_path_to_save,content)
                images_dir = os.path.join(folder_to_store,"images")
                path_to_pdf = f"{folder_to_store}/{get_basepath()}.pdf"
                convert_to_pdf(images_dir,path_to_pdf,self.logger)
            except:
                self.logger.error(f"Error downloading {i}th file of {get_basepath()} url: {get_url(i)}")
                self.logger.warning(f"I suggest you to rerun the program for {self.url}")

if __name__ == "__main__":
    downloader = EapDownloader("https://eap.bl.uk/archive-file/EAP781-1-5-103")
    downloader.convert_to_pdf("Journal/EAP781_1_5_95/images","test.pdf")



