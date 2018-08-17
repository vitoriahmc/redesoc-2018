import os
from time import sleep

from selenium import webdriver


# Baixe o driver de https://sites.google.com/a/chromium.org/chromedriver/downloads
# e extraia o executável. Coloque na constante abaixo o caminho completo para ele.

DRIVER_PATH = r'caminho/completo/incluindo/o/proprio/executavel/nao/pare/na/pasta'

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

SLEEP_TIME = 2

ROOT_USERNAME = 'SEU USERNAME'

DATA_DIR = 'data'


def scrape_friends(browser):
    friends = set()

    while True:
        added = False

        for element in browser.find_elements_by_css_selector(".fsl.fwb.fcb"):
            a = element.find_element_by_tag_name('a')
            href = a.get_attribute('href')

            if ROOT_USERNAME in href:
                continue

            substring = href[25:(href.find('fref') - 1)]

            if substring.startswith('profile.php?id='):
                friend = substring[15:]
            else:
                friend = substring

            if friend not in friends:
                friends.add(friend)
                added = True

        if added:
            browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(SLEEP_TIME)
        else:
            break

    return friends


def save_friends(username, friends):
    path = os.path.join(DATA_DIR, 'facebook', username + '.txt')

    with open(path, 'w', encoding='utf-8') as file:
        for friend in friends:
            file.write(friend + '\n')


def main():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    browser = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    browser.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    browser.get('https://www.facebook.com')
    sleep(SLEEP_TIME)

    browser.find_element_by_id('email').send_keys('SEU LOGIN')
    browser.find_element_by_id('pass').send_keys('SUA SENHA')
    browser.find_element_by_id('loginbutton').click()
    sleep(SLEEP_TIME)

    browser.get('https://www.facebook.com/{}/friends'.format(ROOT_USERNAME))
    sleep(SLEEP_TIME)

    root_friends = scrape_friends(browser)
    save_friends(ROOT_USERNAME, root_friends)

    for username in root_friends:
        browser.get('https://www.facebook.com/{}/friends_mutual'.format(username))
        sleep(SLEEP_TIME)

        elements = browser.find_elements_by_class_name('_3sz')
        texts = [element.text for element in elements]

        if 'Amigos em comum' in texts:
            friends = scrape_friends(browser)
            save_friends(username, friends)


if __name__ == '__main__':
    main()
