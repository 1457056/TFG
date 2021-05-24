import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

usr = "<your_facebook_email_address>"
pwd = "<your_facebook_password>"

url = "https://mobile.facebook.com/story.php?story_fbid=10156391722455952&amp;id=157851205951"
driver = webdriver.Chrome('/Users/zero/Documents/GitHub/SentimentAnalysis/chromedriver')
driver.get(url)

time.sleep(1)
if driver.find_element_by_xpath('//*[@id="viewport"] /div/div[3] /div/div[2]/ div / a'):
    driver.find_element_by_xpath('//*[@id="viewport"] /div/div[3] /div/div[2]/ div / a').click()

elem = driver.find_element_by_id("m_login_email")
elem.send_keys(usr)

elem = driver.find_element_by_id("m_login_password")
elem.send_keys(pwd)

elem.send_keys(Keys.RETURN)

hasLoadMore = True
while hasLoadMore:
    time.sleep(1)
    try:
        if driver.find_element_by_xpath(
                '//*[@id="viewport"] /div/div[4] /div/div/div/div/div/div[2] /div/div/div[5] /*[@class="async_elem"]/ a'):
            driver.find_element_by_xpath('//*[@id="viewport"] /div/div[4] /div/div/div/div/div/div[2] /div/div/div[5] /*[@class="async_elem"]/ a').click()
    except:
        hasLoadMore = False

users_list = []

users = driver.find_elements_by_class_name('_2b05')

for user in users:
    users_list.append(user.text)

i = 0
texts_list = []

texts = driver.find_elements_by_class_name('_2b06')

for txt in texts:
    texts_list.append(txt.text.split(users_list[i]

                                     ))
    i += 1
    comments_count = len(users_list)

for i in range(1, comments_count):
    user = users_list[i]

    text = texts_list[i]

    print("User ", user)
    print("Text ", text)
