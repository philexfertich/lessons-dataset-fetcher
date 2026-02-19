import random

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

import pandas as pd


# >>>>> CONSTS >>>>>
BASE_URL = 'https://www.khanacademy.org/{}'
# <<<<< CONSTS <<<<<


# >>>>> Utils >>>>>
def rnd():
    return int(random.random() * 100) / 100

def wait(time_sec = 0.5 + rnd()):
    global driver
    driver.implicitly_wait(time_sec)

def page(path = ''):
    global driver
    driver.get(BASE_URL.format(path.strip('/')))

def apply_cookies():
    global driver
    global concent_button_tag
    try:
        wait = WebDriverWait(driver, timeout=10+rnd())
        wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, concent_button_tag)))
        driver.find_element(by=By.CSS_SELECTOR, value=concent_button_tag).click()
    except Exception as e:
        print(e)
# <<<<< UTILS <<<<<


# >>>>> Values >>>>>
pages = [
    'math',
    'science',
    'computing'
]
concent_button_tag = 'button#onetrust-reject-all-handler'
# <<<<< Values <<<<< 


# >>>>> Browsing >>>>>
driver = webdriver.Chrome()

page()

wait()

title = driver.title

wait()

apply_cookies()
# <<<<< Browsing <<<<<


# >>>>> FETCHING >>>>>
elements = {
    'Discipline': [],
    'Section': [],
    'Unit': []
}
append = lambda k, v: elements[k].append(v)
for p in pages:
    wait(10 + rnd())
    page(p)
    sections = driver.find_elements(by=By.CLASS_NAME, value='_ja0qep1')
    print(len(sections))

    for s in sections:
        wait()
        wt = WebDriverWait(driver, rnd())
        title = s.find_element(by=By.XPATH, value=".//h2/a")
        # wt.until(ec.visibility_of(title))
        units = s.find_elements(by=By.XPATH, value='.//div/div/a')
        for u in units:
            append('Discipline', p)
            append('Section', title.text)
            text = driver.execute_script("return arguments[0].firstChild.textContent.trim();", u).strip()
            append('Unit', text)
            print((p, title.text, text))
# <<<<< FETCHING <<<<<


# >>>>> FINISHING >>>>>
wait()

driver.quit()
# <<<<< FINISHING <<<<<


# >>>>> SAVING >>>>>
df = pd.DataFrame(data=elements)
df.to_csv('table/units.csv', index=False)
# <<<<< SAVING <<<<<
