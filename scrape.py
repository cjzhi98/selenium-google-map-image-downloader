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

kl = timezone("Asia/Kuala_Lumpur")
now = datetime.now(kl)

url = input("Enter the url: ")

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--window-size=1920x1080")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

driver.get(url)

print("\n========Scraping Photos========\n")
photos = []

time.sleep(5)

photo_page_html = BeautifulSoup(driver.page_source, "html.parser")

photo_elems = photo_page_html.find_all("a", class_="OKAoZd")

last_index = photo_elems[-1]["data-photo-index"]

if int(last_index) >= 6:
    last_index = "6"

img_result = WebDriverWait(driver, 10).until(
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

for photo in photo_elems:
    print(photo)

photos_in_local = []

try:
    for photo in photo_elems[:6]:
        # print(photo)
        photo_link = retrive_ori_photo(parse_photo_link_double(str(photo)))
        resized_photo_link = setPhotoSize(photo_link, 1200)
        photos.append(photo_link)

    print("\n========Downloading Photos========\n")

    photo_num = 0
    for image_url in photos:
        print(image_url)
        photo_name = str(uuid.uuid4()) + ".jpg"
        photo_path = get_download_folder() + photo_name
        photo_num = photo_num + 1
        urllib.request.urlretrieve(image_url, photo_path)
        photos_in_local.append(photo_path)
except Exception as e:
    print(e)
    driver.quit()
    pass

driver.quit()