from selenium import webdriver
from os.path import abspath
from time import sleep
from lxml import html
import tomllib
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import NamedTuple


def load_config() -> dict[str, str]:
    with open('./config.toml', 'rb')  as config_file:
        data = tomllib.load(config_file)
    return data


class StudyGoList(NamedTuple):
    name: str
    left_language: str
    right_language: str
    data: list[tuple[str, str]]


def main(url: str, driver: webdriver.Chrome) -> StudyGoList:
    driver.get(url)
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/main/div/div/div[1]/header/div[2]/h1')))
        sleep(1)
    except Exception as e:  # noqa
        raise e

    name = driver.find_element(
        By.XPATH, '/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[1]/header[1]/div[2]/h1[1]/span[1]').text\
        .replace(' ', '_')
    html_content: html.HtmlElement = html.fromstring(driver.page_source)
    first_row_language: str = \
        html_content.xpath(
            '/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[1]/span[1]/text()')[0]
    second_row_language: str = \
        html_content.xpath(
            '/html[1]/body[1]/div[1]/main[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/span[1]/text()')[0]
    pairs_list: list[html.HtmlElement] = html_content \
                                             .xpath('/html/body/div/main/div/div/div[3]/div')[0] \
                                             .getchildren()[1::]
    pairs_result: list[tuple[str, str]] = []
    for pair in pairs_list:
        pair_row: html.HtmlElement = pair.find_class('content')[0] \
            .find_class('row')[0]
        word_left: str = pair_row.find_class('col s-5 middle info-col')[0] \
            .find_class('info-block')[0] \
            .find_class('info notranslate')[0] \
            .text
        word_right: str = pair_row.find_class('col s-7 middle')[0] \
            .find_class('info hide-xs notranslate')[0] \
            .text
        pairs_result.append((word_left, word_right))

    return StudyGoList(left_language=first_row_language, right_language=second_row_language, data=pairs_result, name=name)


if __name__ == '__main__':
    config = load_config()

    with open(config.get('links_input_file', 'links.txt'), 'r') as file:  # noqa
        links: list[str] = file.read().splitlines()
    flashcards_all: list[StudyGoList] = []
    service = Service(executable_path=config.get('chromedriver_path', 'chromedriver.exe'))
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    if (config_binary_location := config.get('chrome_path', 'AUTOFIND')) != 'AUTOFIND':
        options.binary_location = config_binary_location
    driver = webdriver.Chrome(service=service, options=options)
    for link in links:
        try:
            flashcards_all.append(main(link, driver))
        except Exception as e:
            print(f"Link `{link}` raised an exception during scraping: ", e, ' (this link will be skipped)')
            continue
    flashcard: StudyGoList
    for flashcard in flashcards_all:
        csv_string: str = f'{flashcard.left_language},{flashcard.right_language}\n'
        for left_row, right_row in flashcard.data:
            csv_string += f'{left_row},{right_row}\n'
        with open(f'out/{flashcard.name}.csv', 'w') as file:
            file.write(csv_string)
            print(f"Flashcard {flashcard.name} has been successfully written to {abspath(file.name)}")
    driver.quit()
