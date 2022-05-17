from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep


# Chrome のオプションを設定する
options = webdriver.ChromeOptions()
options.add_argument('--headless')

# Selenium Server に接続する
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=options.to_capabilities(),
    options=options,
)

# Selenium 経由でブラウザを操作する
driver.get('https://yoyaku.city.yokohama.lg.jp/')
sleep(3)
print(driver.current_url)
driver.find_element(By.XPATH, '//*[@id="RSGK001_05"]').click()
sleep(3)
driver.find_element(By.XPATH, '//*[@id="fbox_01"]').click()
sleep(3)
driver.find_element(By.XPATH, '//*[@id="fbox_05"]').click()
sleep(3)
driver.find_element(By.XPATH, '//*[@id="idbtn_next_page"]').click()
sleep(3)
driver.find_element(By.XPATH, '//*[@id="fbox_580"]').click()
sleep(3)
driver.find_element(By.XPATH, '//*[@id="fbox_01"]').click()
sleep(3)
print(driver.page_source)


# ブラウザを終了する
driver.quit()