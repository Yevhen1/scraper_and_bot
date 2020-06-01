import requests
from bs4 import BeautifulSoup as Bs
import os
from multiprocessing import Pool

BASIC_URL = "https://wallpapercave.com"
URL = "https://wallpapercave.com/categories/cars"#change categoties
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}


page = requests.get(URL, headers=headers)
soup = Bs(page.content, 'lxml')
find_block = soup.find_all('a', attrs={'class': 'albumthumbnail'})
folder = 'image'


def get_image_package(s):
    f = Bs(s, 'lxml')
    link = f.find('div', attrs={'class': 'albumphoto'}).get('href')
    try:
        page_0 = requests.get(BASIC_URL + link, headers=headers)
        soup_0 = Bs(page_0.content, 'lxml')
        new_folder = str(folder + link)
        os.mkdir(new_folder)
        image = soup_0.find_all('div', attrs={'class': 'wallpaper'})
        for im in image:
            pic = im.find('img', attrs={'class': 'wpimg'}).get('src')
            r = requests.get(BASIC_URL + pic, stream=True)
            with open(new_folder + pic[pic.index('/wp/') + 3: len(pic)], 'bw') as fa:
                for chunk in r.iter_content(20000):
                    fa.write(chunk)
    except Exception as exs:
        print(exs)


if __name__ == "__main__":
    if not os.path.exists(folder):
        os.mkdir(folder)
    new_block = []
    for i in range(172, find_block.__len__()):
        new_block.append(str(find_block[i]))
    with Pool(25) as p:
        p.map(get_image_package, new_block)
        p.close()
        p.join()


