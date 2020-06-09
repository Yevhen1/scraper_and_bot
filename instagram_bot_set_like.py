from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import random
from random import randint
from time import sleep

USER_NAME = "user_name"
PASSWORD = "password"
HASH_TAG_CAR = ['tag_1', 'tag_2', 'tag_3', 'tag_4']


def driver_init(visible=True):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    if visible:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.set_window_size(1200, 900)
    return driver


class InsBot:
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        self.driver = driver_init()
        self.driver.get("https://www.instagram.com/")

    def log_in(self):
        sleep(2)
        user_name_elem = self.driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.user_name)
        password_elem = self.driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        sleep(6)

    def start(self, hash_tags):
        all_like = 0
        for tag in hash_tags:
            pic_href = []
            print(tag)
            try:
                self.driver.get("https://www.instagram.com/explore/tags/" + tag + "/")
                sleep(2)
                for n in range(4):
                    try:
                        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        sleep(2)
                        # get tags
                        href_in_view = self.driver.find_elements_by_tag_name('a')
                        # finding relevant hrefs
                        href_in_view = [elem.get_attribute('href') for elem in href_in_view
                                        if '.com/p/' in elem.get_attribute('href')]
                        [pic_href.append(href) for href in href_in_view if href not in pic_href]
                        print("Check: pic href length " + str(len(pic_href)))
                    except Exception as e:
                        print(e)
                        continue
            except Exception as e:
                print(e)
                continue
            print(pic_href.__sizeof__())
            number = 0
            like_set = 0
            for pic in pic_href:
                try:
                    self.driver.get(pic)
                    sleep(randint(2, 4))
                    # set like
                    if randint(1, 100) < 50 and self.driver.find_element_by_class_name('_8-yf5 ').\
                            get_attribute('fill') == "#ed4956":
                        self.driver.find_element_by_class_name('wpO6b ').click()
                        like_set += 1
                        all_like += 1
                        sleep(randint(1, 2))
                    number += 1
                    print(number)
                except Exception as e:
                    sleep(2)
                    print(e)
            if all_like > 300:
                print(all_like)
                break
            sleep(15)
            print('hove to be like set: - ', all_like)

    def stop(self):
        self.driver.close()


if __name__ == "__main__":
    b = InsBot(USER_NAME, PASSWORD)
    b.log_in()
    b.start(HASH_TAG_CAR)
    sleep(10)
    b.stop()
