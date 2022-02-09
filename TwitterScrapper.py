import csv
from getpass import getpass
from time import sleep
from selenium.webdriver import Safari, Chrome, Firefox, Ie
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select, WebDriverWait


class TwitterScrapper:
    SAFARI = 1
    CHROME = 2
    FIREFOX = 3

    def __init__(self):
        self.__browser = None
        self.__tweets = None
        self.__search = None
        self.__bunch = []
        self.__tweets_list = []

    def setBrowser(self, brow):
        if brow == 1:
            self.__browser = Safari()
        elif brow == 2:
            self.__browser = Chrome()
        elif brow == 3:
            self.__browser = Firefox()
        else:
            self.__browser = None

    def open(self):
        if self.__browser is not None:
            self.__browser.get('https://twitter.com/i/flow/login')
            self.__browser.implicitly_wait(10)
            self.__browser.maximize_window()
        else:
            print('Browser not initialized!!')

    def enterUsername(self, mail):
        try:
            name = self.__browser.find_element_by_name('username')
            name.send_keys(str(mail))
            name.send_keys(Keys.RETURN)
        except NoSuchElementException:
            return

    def enterPassword(self, password):
        try:
            passText = self.__browser.find_element_by_name('password')
            passText.send_keys(password)
            passText.send_keys(Keys.RETURN)
        except NoSuchElementException:
            return

    def enterPhoneNo(self, phone):
        try:
            passText = self.__browser.find_element_by_name('text')
            passText.send_keys(phone)
            passText.send_keys(Keys.RETURN)
        except NoSuchElementException:
            return

    def search(self, topic):
        try:
            search_input = self.__browser.find_element_by_xpath('//input[@aria-label="Search query"]')
            search_input.send_keys(topic)
            search_input.send_keys(Keys.RETURN)
            self.__search = topic
        except NoSuchElementException:
            return

    def latest(self):
        try:
            self.__browser.find_element_by_link_text('Latest').click()
        except NoSuchElementException:
            return

    def people(self):
        try:
            self.__browser.find_element_by_link_text('People').click()
        except NoSuchElementException:
            return

    def photos(self):
        try:
            self.__browser.find_element_by_link_text('Photos').click()
        except NoSuchElementException:
            return

    def videos(self):
        try:
            self.__browser.find_element_by_link_text('Videos').click()
        except NoSuchElementException:
            return

    def tweets(self):
        try:
            if self.__search is not None:
                self.__tweets = self.__browser.find_elements_by_xpath('//article[@data-testid="tweet"]')
        except NoSuchElementException:
            return

    def signUp(self):
        div = self.__browser.find_elements_by_xpath('.//div[@data-testid="logInSignUpFooter"]')
        div[0].find_element_by_xpath('.//span/span').click()

    def get_Tweet_Bunch(self, tweet):
        try:
            name = tweet.find_element_by_xpath('.//span').text
            id_ = tweet.find_element_by_xpath('.//span[contains(text(), "@")]').text
            comment = tweet.find_element_by_xpath('.//div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]').text
            replyTo = tweet.find_element_by_xpath('.//div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[2]').text
            content = comment + replyTo
            try:
                time = tweet.find_element_by_xpath('.//time').get_attribute('datetime')
            except NoSuchElementException:
                return
            reply = tweet.find_element_by_xpath('.//div[@data-testid="reply"]').text
            likes = tweet.find_element_by_xpath('.//div[@data-testid="like"]').text
            retweets = tweet.find_element_by_xpath('.//div[@data-testid="retweet"]').text
            if content not in self.__bunch:
                self.__bunch.append(content)
                tweets_data = (name, id_, time, content, reply, likes, retweets)
                self.__tweets_list.append(tweets_data)
        except StaleElementReferenceException:
            return

    def signInWithGoogle(self):
        self.__browser.find_element_by_xpath('.//div[@aria-label="Sign in with Google"]').click()

    def advanceSearch(self):
        try:
            self.__browser.find_element_by_link_text('Advanced search').click()
        except NoSuchElementException:
            return

    def languageFilter(self, language):
        element = WebDriverWait(self.__browser, 10).until(
            lambda driver: driver.find_element_by_xpath('//select[@aria-labelledby="SELECTOR_1_LABEL"]'))
        element.send_keys(Keys.RETURN)
        select = Select(element)
        select.select_by_visible_text(language)
        searchList = WebDriverWait(self.__browser, 10)\
            .until(lambda driver: driver.find_elements_by_class_name('r-qvutc0'))
        search = None
        for s in searchList:
            if s.text == 'Search':
                search = s
                break
        search.click()

    def lastPosition(self):
        return self.__browser.execute_script("return window.pageYOffset;")

    def scroll(self):
        self.__browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def addGmail(self, mail):
        try:
            name = self.__browser.find_element_by_name('identifier')
            name.send_keys(mail)
            name.send_keys(Keys.RETURN)
        except NoSuchElementException:
            return

    @property
    def tweetList(self):
        return self.__tweets

    @property
    def tweetBunch(self):
        return self.__bunch

    @property
    def tweet_List(self):
        return self.__tweets_list

    @property
    def browser(self):
        return self.__browser

    def saveCSV(self, name):
        with open(name, 'w', newline='', encoding='utf-8') as f:
            header = ['Name', 'Username', 'Timestamp', 'Tweets', 'Reply', 'Likes', 'Retweets']
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(self.__tweets_list)

    def exit(self):
        self.__browser.quit()
