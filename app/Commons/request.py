import requests


def makeGet(url):
    response = requests.get(url)
    return response

async def makeParallelGet(session, url):
    async with session.get(url) as response:
        print(f"Downloading file from {url}")
        return {
            "status":response.status,
            "content_length":response.content_length,
            "content":await response.read()
        }

def makeRequest(url,method="POST"):
    if method == "POST":
        pass
    else:
        return makeGet(url)

if __name__ == "__main__":
    print(makeGet("https://images.eap.bl.uk/EAP781/EAP781_1_5_98/100.jp2/full/100000000,/0/default.jpg").status_code==200)