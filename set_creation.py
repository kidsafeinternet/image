import os
import shutil
import urllib.request
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import threading
from tqdm import tqdm

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

    def download_image(self, img_url, filename, subdir, pbar):
        try:
            urllib.request.urlretrieve(img_url, filename)
            shutil.move(filename, f"{self.directory}/{subdir}")
            pbar.update(1)
        except Exception as e:
            print(f"Failed to download {img_url}. Reason: {e}")

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

        # Progress bar
        with tqdm(total=n) as pbar:
            threads = []

            # Extract image URLs and download concurrently
            while len(threads) < n:
                img_tags = driver.find_elements(By.TAG_NAME, "img")
                for img in img_tags:
                    img_url = img.get_attribute("src")
                    if img_url and len(threads) < n:
                        filename = f"img{len(threads)}.jpg"
                        thread = threading.Thread(target=self.download_image, args=(img_url, filename, subdir, pbar))
                        threads.append(thread)
                        thread.start()

                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
                time.sleep(2)  # Wait for new images to load

            driver.quit()

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

        print("Crawl complete")