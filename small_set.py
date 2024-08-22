from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import shutil
import urllib.request
import time

# URL of the site
url = 'https://www.unsplash.com'
url2 = 'https://reddtastic.com/r/nsfw'

DIR = 'small_set'

# Crawl
def crawl(url, n, subdir, dir='small_set'):
    # Check if subdir of 'small_set' exists, if not, create it
    if not os.path.exists(f'{dir}/{subdir}'):
        os.makedirs(f'{dir}/{subdir}')
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless')  # Run in headless mode
    driver = webdriver.Chrome(options=options)
    
    # Load the webpage
    driver.get(url)

    # Wait for the page to load
    time.sleep(2)
    
    # Extract image URLs
    img_tags = driver.find_elements(By.TAG_NAME, 'img')
    urls = [img.get_attribute('src') for img in img_tags if img.get_attribute('src')]

    driver.quit()
    
    if len(urls) < n:
        print(f'Not enough images found on {url}. Found {len(urls)} images.')
        return
    
    for i in range(n):
        img = urls[i]
        filename = 'img' + str(i) + '.jpg'
        urllib.request.urlretrieve(img, filename)
        shutil.move(filename, f'{dir}/' + subdir)
        print(f'Image {i} downloaded')
    print('Crawl complete')

# Create a directory
if not os.path.exists(DIR):
    os.makedirs(DIR)
else:
    shutil.rmtree(DIR)

# Crawl 5 images from the site
if __name__ == '__main__':
    crawl(url, 5, 'sfw', DIR)
    crawl(url2, 5, 'nsfw', DIR)