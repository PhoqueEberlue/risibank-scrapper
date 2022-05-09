import shutil
from typing import List
from database import Database
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
import requests


class Scrapper:
    def __init__(self, database):
        """
        Bot class
        """
        self.driver = webdriver.Firefox()
        self.database: Database = database

    def search(self, tags: List[str]):
        """
        Run the bot
        """
        self.driver.get(f"https://risibank.fr/recherche/tag/{'-'.join(tags)}")

        elements = WebDriverWait(self.driver, timeout=2).until(
            lambda d: d.find_elements(by=By.CLASS_NAME, value="media-image"))

        links = []
        for element in elements:
            links.append(element.get_attribute("href"))

        for link in links:
            media = self.fetch_media(link)
            self.download_img(media['id_media'], media['img_full_link'])
            self.database.add_media(media)

    def fetch_media(self, url):
        self.driver.get(url)
        res = {}

        i = 1
        for key in ["id_media", "date_ajout", "auteur", "categorie", "tags", "img_full_link", "thumbnail_link", "source_link"]:
            data: WebElement = WebDriverWait(self.driver, timeout=5).until(
                lambda d: d.find_element(by=By.CSS_SELECTOR,
                                         value="body > div:nth-child(1) > "
                                               "div.main-content.container-sm.row.m-auto.px-0 "
                                               "> div.col-lg-7.mb-4 > div > div:nth-child(6) > table > tbody > "
                                               f"tr:nth-child({i}) > td:nth-child(2)"))
            match key:
                case "id_media":
                    res[key] = data.get_attribute("innerText")
                case "date_ajout":
                    res[key] = data.get_attribute("innerText")
                case "auteur":
                    a_elem = data.find_element_by_css_selector('a')
                    res[key] = a_elem.get_attribute('textContent')
                case "categorie":
                    res[key] = data.get_attribute("innerText")
                case "tags":
                    res[key] = data.get_attribute("innerText").split(' ')
                case "img_full_link":
                    a_elem = data.find_element_by_css_selector('a')
                    res[key] = a_elem.get_attribute("href")
                case "thumbnail_link":
                    a_elem = data.find_element_by_css_selector('a')
                    res[key] = a_elem.get_attribute("href")
                case "source_link":
                    a_elem = data.find_element_by_css_selector('a')
                    res[key] = a_elem.get_attribute("href")

            if i == 7:
                i += 2
            else:
                i += 1
        return res

    @staticmethod
    def download_img(id_media, link):
        r = requests.get(link, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True

            with open(f"../img/{str(id_media)}.jpg", 'wb') as f:
                shutil.copyfileobj(r.raw, f)
        else:
            print("Erreur, l'image n'a pas pu etre recupere")
