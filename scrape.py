# Scrape Photos
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime
import time
from helpers import *
from pytz import timezone
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import uuid
import urllib.request
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

kl = timezone("Asia/Kuala_Lumpur")
now = datetime.now(kl)

url = input("Enter the url: ")

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(options=options)

driver.get(url)

print("\n========Scraping Photos========\n")
photos = []

time.sleep(5)

first_img = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (
            By.XPATH,
            "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div[1]/div[1]/div/a/div[2]",
        )
    )
)

photo_page_html = BeautifulSoup(driver.page_source, "html.parser")

photo_elems = photo_page_html.find_all("a", class_="OKAoZd")

last_index = photo_elems[-1]["data-photo-index"]

if int(last_index) >= 6:
    last_index = "6"

img_result = WebDriverWait(driver, 60).until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            f"a[data-photo-index='{last_index}']",
        )
    )
)
driver.execute_script("arguments[0].scrollIntoView(true);", img_result)

time.sleep(5)

photo_page_html = BeautifulSoup(driver.page_source, "html.parser")

photo_elems = photo_page_html.find_all("div", class_="U39Pmb")


photos_in_local = []

try:
    photo_num = 0
    print(photo_num)
    for photo in photo_elems[:20]:
        try:
            photo_link = retrive_ori_photo(parse_photo_link_double(str(photo)))
            resized_photo_link = setPhotoSize(photo_link, 1200)
            if "/p/" in resized_photo_link:
                photos.append(resized_photo_link)
                photo_num = photo_num + 1
                print(photo_num)
                if photo_num == int(last_index):
                    break
        except:
            print("Error")
            continue

    print("\n========Downloading Photos========\n")

    for image_url in photos:
        print(image_url)
        photo_name = str(uuid.uuid4()) + ".jpg"
        photo_path = get_download_folder() + photo_name
        urllib.request.urlretrieve(image_url, photo_path)
        photos_in_local.append(photo_path)

except Exception as e:
    driver.quit()
    pass

driver.quit()
