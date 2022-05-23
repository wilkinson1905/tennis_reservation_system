from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
import traceback
import datetime
import yaml


def get_availability_dict(html): ## => year, month, availability_dict{day:["○" or "×"]}
    soup = BeautifulSoup(html, 'html.parser')
    ## 年月の取得
    year_and_month = soup.find_all("option", attrs={"selected":"selected"})
    year = year_and_month[0]["value"]
    month = year_and_month[1]["value"]
    ## 空き状況の取得
    results = soup.find(id="calendar").find_all("td")
    availability_dict = {}
    for result in results:
        full = result.find("p",class_="end")
        available = result.find("input")
        if full is not None:
            ## 予約が埋まっている日の処理
            day = full.get_text()
            if day == "-":
                continue
            availability_dict[day] = "full"
        elif available is not None:
            ## 予約が空いている日の処理
            day = available["value"]
            availability_dict[day] = "empty"
    return int(year),int(month), availability_dict

## Chrome のオプションを設定する
options = webdriver.ChromeOptions()
options.add_argument('--headless')

## Selenium Server に接続する
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=options,
)

## Selenium 経由でブラウザを操作する
while True:
    try:
        all_availability_info = {}
        driver.implicitly_wait(10)
        driver.get('https://yoyaku.city.yokohama.lg.jp/')
        ## 港北スポーツセンターのカレンダーを取得
        driver.find_element(By.XPATH, '//*[@id="RSGK001_05"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_01"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_05"]').click()
        driver.find_element(By.XPATH, '//*[@id="idbtn_next_page"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_580"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_01"]').click()
        driver.find_element(By.XPATH, '//*[@id="calendar"]')
        year, month, availability_dict = get_availability_dict(driver.page_source)
        all_availability_info[f"{year}_{month}"] = availability_dict
        ## 次の月を取得
        date_now = datetime.datetime.now()
        if date_now.month == month:
            driver.find_element(By.XPATH, '//*[@id="FRM_RSGK305"]/div[3]/div/div/table[1]/tbody/tr/td[9]/button/img').click()
        else:
            driver.find_element(By.XPATH, '//*[@id="FRM_RSGK305"]/div[3]/div/div/table[1]/tbody/tr/td[1]/button/img').click()
        driver.find_element(By.XPATH, '//*[@id="calendar"]')
        year, month, availability_dict = get_availability_dict(driver.page_source)
        all_availability_info[f"{year}_{month}"] = availability_dict
        with open("calendars/kouhoku.yaml", "w") as f:
            yaml.dump(all_availability_info, f)

        driver.get('https://yoyaku.city.yokohama.lg.jp/')
        ## 横浜公園のカレンダーを取得
        driver.find_element(By.XPATH, '//*[@id="RSGK001_05"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_01"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_05"]').click()
        driver.find_element(By.XPATH, '//*[@id="idbtn_next_page"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_570"]').click()
        driver.find_element(By.XPATH, '//*[@id="fbox_00"]').click()
        driver.find_element(By.XPATH, '//*[@id="calendar"]')
        year, month, availability_dict = get_availability_dict(driver.page_source)
        all_availability_info[f"{year}_{month}"] = availability_dict
        ## 次の月を取得
        date_now = datetime.datetime.now()
        if date_now.month == month:
            driver.find_element(By.XPATH, '//*[@id="FRM_RSGK305"]/div[3]/div/div/table[1]/tbody/tr/td[9]/button/img').click()
        else:
            driver.find_element(By.XPATH, '//*[@id="FRM_RSGK305"]/div[3]/div/div/table[1]/tbody/tr/td[1]/button/img').click()
        driver.find_element(By.XPATH, '//*[@id="calendar"]')
        year, month, availability_dict = get_availability_dict(driver.page_source)
        all_availability_info[f"{year}_{month}"] = availability_dict
        with open("calendars/yokohama.yaml", "w") as f:
            yaml.dump(all_availability_info, f)


    except:
        traceback.print_exc()
    break

## ブラウザを終了する
driver.quit()