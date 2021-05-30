import os
import img2pdf
import glob
from requests.api import get 
from urllib.parse import urlparse


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)


def read_txt_file(filepath):
    
    with open(filepath,'r') as myFile:
        content = myFile.read()
    return content.split('\n')

def create_base_link_for_eap(url):
    base = urlparse(url).path.split('/')[-1]
    base_1 = base.split('-')[0]
    base_2 = '_'.join(base.split('-')[1:])

    def get_url(image_no,quality=10000,rotation=0):
        return f"https://images.eap.bl.uk/{base_1}/{base_1}_{base_2}/{image_no}.jp2/full/{quality},/{rotation}/default.jpg"

    def get_path():
        return f"{base_1}_{base_2}"
        

    return get_url,get_path

def save_file(path,content):
    with open(path,'wb') as f:
        f.write(content)

def find_pdf_link(links):
    for each_link in links:
        base_name = os.path.basename(each_link["link"])
        if base_name.split('.')[-1] == "pdf":
            return f"https://archive.org{each_link['link']}"
    else:
        return False

def convert_to_pdf(path_to_images,path_to_pdf,logger):
    images = glob.glob(f"{path_to_images}/*.jpg",recursive=True)
    logger.info("Creating pdf")
    with open(path_to_pdf,"wb") as f:
        f.write(img2pdf.convert(images))


if __name__ == "__main__":
    url = "https://eap.bl.uk/archive-file/EAP781-1-5-102"
    base_url = create_base_link_for_eap(url)
    print(base_url(1))