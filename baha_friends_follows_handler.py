# -*- coding: UTF-8 -*-

import logging
import random
import re
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BahaFriends():
    follows = {
        '0': '叭',
        '1': '哈',
        '2': '創',
        '3': '推',
        '5': '實'
    }

    def __init__(self, command):
        """Init selenium chrome browser."""
        logging.info('Starting..')
        if len(command) != 5:
            logging.error('Command need 5 chars.')
            return
        else:
            for i in range(len(command)):
                if command[i] not in ['-', '0', '1']:
                    logging.error('Command can only use [-, 0, 1].')
                    return
        driver = webdriver.Chrome(r'.\tool\chromedriver.exe')
        driver.maximize_window()

        self.command = command
        self.driver = driver
        self.nums = ['0', '1', '2', '3', '5']
        self.exclude_ids = []
        self.get_exclude_baha_id()
        self.baha_login()
        self.get_baha_friends_info()
        self.baha_friends_process()

    def baha_login(self):
        """Wait for user to log in."""
        url = 'https://user.gamer.com.tw/login.php'

        while not self.driver.get_cookie('BAHAID'):
            self.driver.get(url)
            # Wait for user logging and going back to home page
            WebDriverWait(self.driver, 300, 10).until(
                EC.url_matches('https://www.gamer.com.tw/'))
            baha_id = self.driver.get_cookie('BAHAID')
        logging.info('Logged In. ID = %s', baha_id['value'])

        url = 'https://home.gamer.com.tw/friendList.php?user=' \
            + baha_id['value'] + '&t=3'
        self.driver.get(url)
        logging.info('Go to %s', url)
        WebDriverWait(self.driver, 10, 2).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'user_id')))

    def get_baha_friends_info(self):
        """Get baha friends info."""
        logging.info('Getting baha friends info.')
        self.friends_id = self.driver.find_elements_by_class_name('user_id')
        friends_follow_btn = []
        for i in range(5):
            if self.command[i] != '-':
                target = 'follow' + self.nums[i]
                friends_follow_btn.append(
                    self.driver.find_elements_by_name(target))
            else:
                friends_follow_btn.append(None)
        self.friends_follow_btn = friends_follow_btn

    def baha_friends_process(self):
        """Handle each baha friend follow state."""
        logging.info('Processing..')
        try:
            for index, element in enumerate(self.friends_id):
                if element.text in self.exclude_ids:
                    logging.info('(No.%d) Ignore ID: %s', index, element.text)
                    continue
                # Wait for some seconds each time
                time.sleep(random.random() + 2)
                for i in range(5):
                    if self.command[i] != '-':
                        time.sleep(0.2)
                        self.baha_friends_process_change_state(index,
                                                               element.text,
                                                               i)
                logging.info('(No.%d) ID: %s Done.', index, element.text)
            logging.info('Finished.')
        except (NoSuchElementException, TimeoutException):
            pass
        finally:
            logging.info('Closing browser..')
            time.sleep(3)
            self.driver.quit()
            logging.info('Browser closed.')

    def baha_friends_process_change_state(self, friends_index, friend_id, num):
        """Change baha friends follow state."""
        target = 'fState' + friend_id + '_' + self.nums[num]
        prev = self.driver.find_element_by_name(
            target).get_attribute('value')
        if self.command[num] != prev:
            self.driver.execute_script(
                'arguments[0].click();',
                self.friends_follow_btn[num][friends_index])
            curr = self.driver.find_element_by_name(
                target).get_attribute('value')

            logging.info('ID: %s, %s changed from %s to %s.',
                         friend_id, self.follows[self.nums[num]],
                         prev, curr)

    def get_exclude_baha_id(self):
        """Read ids from text file that need to be ignored."""
        with open('exclude_ids.txt', mode='r', encoding='utf-8') as f:
            ids = []
            illegal_ids = []
            for line in f.readlines():
                if re.search('^([a-zA-Z])([a-zA-Z0-9]){1,11}$', line.strip()):
                    ids.append(line.strip())
                else:
                    illegal_ids.append(line.strip())

        self.exclude_ids = ids
        logging.info('Exclude IDs: %s', self.exclude_ids)
        logging.warning('Illegal IDs in exclude IDs: %s', illegal_ids)


def init_log():
    """Init the logger."""
    FORMAT = '%(asctime)-20s %(levelname)-9s %(message)s'
    DATEFORMAT = '%Y-%m-%d %H:%M:%S'
    handler = logging.FileHandler("log.log", mode='w', encoding="utf-8")
    logging.basicConfig(handlers=[handler],
                        format=FORMAT,
                        datefmt=DATEFORMAT,
                        level=logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATEFORMAT))
    logging.getLogger().addHandler(console)


if __name__ == "__main__":
    init_log()
    # '叭哈創推實'
    # -: keep the same, 0: change to unsubscribe, 1: change to subscribe
    BAHA = BahaFriends('----0')
    logging.info('End.')
