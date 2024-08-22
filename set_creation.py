import os
import shutil
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


class dataset:
    def __init__(self, directory, n):
        self.directory = directory
        self.n = n
        DIR = self.directory

        # Create a directory
        if not os.path.exists(DIR):
            os.makedirs(DIR)
        else:
            # Remove the contents of the directory, but not .gitignore
            for filename in os.listdir(DIR):
                if filename != ".gitignore":
                    file_path = os.path.join(DIR, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(f"Failed to delete {file_path}. Reason: {e}")

    def crawl(self, url, subdir):
        dir = self.directory
        n = self.n
        # Check if subdir exists, if not create it
        if not os.path.exists(f"{dir}/{subdir}"):
            os.makedirs(f"{dir}/{subdir}")
        driver = webdriver.Chrome()

        # Load the webpage
        driver.get(url)

        # Wait for the page to load
        time.sleep(2)

        # Extract image URLs
        img_tags = driver.find_elements(By.TAG_NAME, "img")
        urls = [
            img.get_attribute("src") for img in img_tags if img.get_attribute("src")
        ]

        # Scroll until enough images are found
        while len(urls) < n:
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(2)  # Wait for new images to load
            img_tags = driver.find_elements(By.TAG_NAME, "img")
            new_urls = [
                img.get_attribute("src") for img in img_tags if img.get_attribute("src")
            ]
            urls.extend(new_urls)
            urls = list(set(urls))  # Remove duplicates

        driver.quit()

        if len(urls) < n:
            print(f"Not enough images found on {url}. Found {len(urls)} images.")
            return

        for i in range(n):
            img = urls[i]
            filename = "img" + str(i) + ".jpg"
            urllib.request.urlretrieve(img, filename)
            shutil.move(filename, f"{dir}/" + subdir)
            print(f"Image {i} downloaded")
        print("Crawl complete")