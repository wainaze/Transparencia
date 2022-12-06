import time
from bs4 import BeautifulSoup
from selenium import webdriver

#function that uses the VAT number to look up result in "banque centrale des bilans"
#HTML signs for finding if the accounts is empty or full
#class="block-results__empty ng-star-inserted" -- NO RESULTS
#class="block-results__items ng-star-inserted" -- ACCOUNTS AVAILABLE

def cbb_result(url):
    driver = webdriver.Chrome()
    #driver.maximize_window()
    driver.get(url)

    time.sleep(1)
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content,"html.parser")
    no_result = soup.findAll ("p", {"class": "empty-state__text"})
    year = soup.find("div", {"id": "userDepositEndDate"})
    driver.quit()

    if no_result:
        a = 'No accounts available'
    elif year:
        a = year.getText()
    else:
        a = "Company number error"
    #print(a)   
    return a

    #test git