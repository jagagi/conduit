from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

from help_sheet import *

URL = 'http://localhost:1667'

class TestConduitapp(object):
    def setup(self):
        browser_options = Options()
        browser_options.headless = True
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=browser_options)
        self.driver.get(URL)

    def teardown(self):
        self.driver.quit()


###########Test1_REGISTRATION

    def test_registration(self):
        self.driver.find_element_by_xpath('//a[@href="#/register"]').click()
        self.driver.find_element_by_xpath('//input[@placeholder="Username"]').send_keys("Leille")
        self.driver.find_element_by_xpath('//input[@placeholder="Email"]').send_keys("jageragnes01+42@gmail.com")
        self.driver.find_element_by_xpath('//input[@placeholder="Password"]').send_keys("Progmasters2021")

        time.sleep(4)

        self.driver.find_element_by_xpath('//button').click()

        success = WebDriverWait(
            self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ('/html/body/div[2]/div/div[3]')))
        )
        assert success.text == "Your registration was successful!"

        self.driver.find_element_by_xpath('//button[@class="swal-button swal-button--confirm"]').click()
        time.sleep(2)

###########Test2_LOGIN

    def test_login(self):
        self.driver.find_element_by_xpath('//a[@href="#/login"]').click()
        self.driver.find_element_by_xpath('//input[@placeholder="Email"]').send_keys("jageragnes01+42@gmail.com")
        self.driver.find_element_by_xpath('//input[@placeholder="Password"]').send_keys("Progmasters2021")

        sign_in_button = WebDriverWait(
            self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ('//form/button')))
        )
        sign_in_button.click()

        time.sleep(4)

        proof = self.driver.find_element_by_xpath("//a[@href = '#/settings']")

        element = WebDriverWait(
            self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href = '#/settings']"))
        )
        assert proof.text == " Settings"

###########Test3_LOGOUT
    def test_logout(self):
        login(self.driver)

        logout_button = WebDriverWait(
            self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ('//i[@class="ion-android-exit"]')))
        )
        logout_button.click()

        buttonlogin = WebDriverWait(
            self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, ('//*[@href="#/login"]')))
        )

        assert buttonlogin.text == 'Sign in'

###########Test4_COOKIES

    def test_cookies(self):

        beforecookies = self.driver.get_cookies()
        numberofbeforecookies = (len(beforecookies))

        acceptbutton = self.driver.find_element_by_xpath('//div[@id="cookie-policy-panel"]//button[2]')
        acceptbutton.click()

        time.sleep(4)

        aftercookies = self.driver.get_cookies()
        numberofaftercookies = (len(aftercookies))

        assert numberofaftercookies > numberofbeforecookies

###########Test5_MULTIPLEPAGES

    def test_multiplepages(self):
        login(self.driver)

        yourfeed = self.driver.find_element_by_xpath("//a[@href = '#/my-feed']")
        yourfeed.click()
        firstarticle = self.driver.find_element_by_xpath('//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/div[1]')

        time.sleep(4)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(4)
        secondpage = self.driver.find_element_by_xpath('//ul[@class="pagination"]/li[2]/a')
        secondpage.click()

        secondpagefirstarticle = self.driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[2]/div/div[1]/div[2]/div/div/div')
        assert firstarticle != secondpagefirstarticle

###########Test6_NEWDATA

    def test_createnewarticle(self):
        login(self.driver)
        self.driver.find_elements_by_xpath('//a[@class="nav-link"]')[0].click()
        time.sleep(4)

        self.driver.find_element_by_xpath('//input[@placeholder="Article Title"]').send_keys(
        "Test article title")
        self.driver.find_elements_by_xpath('//form//input')[1].send_keys("About article")
        self.driver.find_element_by_xpath(
        '//form//textarea[@placeholder="Write your article (in markdown)"]').send_keys(
        "Content of article")

        self.driver.find_element_by_xpath('//button[normalize-space(text()="Publish Article")]').click()
        time.sleep(4)
        deletebutton = self.driver.find_element_by_xpath('//span[contains(text(),"Delete")]')
        assert deletebutton.text == " Delete Article"

###########Test7_DELETEDATA

    def test_deletearticle(self):
        login(self.driver)
        newarticle(self.driver)

        home = self.driver.find_element_by_xpath("//a[@href = '#/']")
        home.click()

        time.sleep(4)

        yourfeed = self.driver.find_element_by_xpath("//a[@href = '#/my-feed']")
        yourfeed.click()

        beforetitles = self.driver.find_elements_by_xpath("//a[@class = 'preview-link']/h1")
        numberofbefortitles = (len(beforetitles))

        time.sleep(4)

        madearticle = self.driver.find_element_by_xpath("//a[@href = '#/articles/test-article-title']")
        madearticle.click()

        time.sleep(4)

        deletebutton = self.driver.find_element_by_xpath('//span[contains(text(),"Delete")]')
        deletebutton.click()

        time.sleep(4)

        okbutton = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[4]/div/button')
        okbutton.click()

        home = self.driver.find_element_by_xpath("//a[@href = '#/']")
        home.click()

        time.sleep(4)

        yourfeed.click()

        aftertitles = self.driver.find_elements_by_xpath("//a[@class = 'preview-link']/h1")
        numberofaftertitles = (len(aftertitles))

        assert numberofbefortitles != numberofaftertitles

###########Test8_MODIFYDATA

    def test_modifydata(self):
        login(self.driver)

        self.driver.find_element_by_xpath("//a[@href = '#/settings']").click()

        time.sleep(4)

        self.driver.find_element_by_xpath('//input[@placeholder="URL of profile picture"]').send_keys(
        "https://upload.wikimedia.org/wikipedia/commons/3/3f/Spiders_web.svg")

        time.sleep(4)

        self.driver.find_element_by_xpath('//button[@class="btn btn-lg btn-primary pull-xs-right"]').click()

        time.sleep(4)

        successfulupdate = self.driver.find_element_by_xpath('/html/body/div[2]/div/div[2]')
        assert successfulupdate.text == "Update successful!"

###########Test9_LISTDATA

    def test_listdata(self):

        tags = self.driver.find_elements_by_xpath("//div[@class='sidebar']/div/a")
        list_of_tags = []
        for i in tags:
            list_of_tags.append(i.text)
        print(list_of_tags)

        assert len(list_of_tags) == len(tags)

###########Test10_DATAFROMSOURCE

    def test_datafromsource(self):
        login(self.driver)
        newarticle(self.driver)

        time.sleep(4)

        with open("datafromsource.txt", "r") as f:
            comments = f.readlines()
            for i in comments:
                self.driver.refresh()
                time.sleep(4)
                writecomment = self.driver.find_element_by_xpath("//textarea[@placeholder='Write a comment...']")
                time.sleep(4)
                writecomment.send_keys(i)

                time.sleep(4)

                commentbutton = self.driver.find_element_by_xpath("//button[text()='Post Comment']")

                time.sleep(4)
                commentbutton.click()

                time.sleep(4)

        cards = self.driver.find_elements_by_xpath("//div[@class='card']")

        assert len(cards) == 4

###########Test11_SAVEDATA

    def test_savedata(self):
        tags = self.driver.find_elements_by_xpath("//div[@class='sidebar']/div/a")

        with open("text.txt", "w") as f:
            for i in tags:
                f.write(i.text + "\n")

        with open("text.txt", "r") as g:
            tagss = g.readlines()
            number_of_tags = 0
            for i in tagss:
                number_of_tags = number_of_tags + 1

        print(number_of_tags)
        print(len(tags))

        assert number_of_tags == len(tags)
