import time

def login(driver):
    login = driver.find_element_by_xpath("//a[@href = '#/login']")
    login.click()

    email = driver.find_element_by_xpath('//input[@placeholder="Email"]')
    email.send_keys("jageragnes01+42@gmail.com")
    password = driver.find_element_by_xpath('//input[@placeholder="Password"]')
    password.send_keys("Progmasters2021")
    signinbutton = driver.find_element_by_xpath('//form/button')
    signinbutton.click()

    time.sleep(4)

def newarticle(driver):
    newarticle = driver.find_element_by_xpath("//a[@href ='#/editor']")
    newarticle.click()

    time.sleep(2)

    title = driver.find_element_by_xpath('//*[@id="app"]//fieldset[1]/input')
    title.send_keys("Test article title")

    about = driver.find_element_by_xpath('//*[@id="app"]//fieldset[2]/input')
    about.click()
    about.send_keys("About article")

    article = driver.find_element_by_xpath('//*[@id="app"]//fieldset[3]/textarea')
    article.click()
    article.send_keys("Content of article")

    publish = driver.find_element_by_xpath('//*[@id="app"]//form/button')
    publish.click()

    time.sleep(2)