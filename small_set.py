from set_creation import dataset

# Crawl 5 images from the site
if __name__ == '__main__':
    d = dataset("small_set", 10)
    d.crawl("https://reddtastic.com/r/nsfw", "nsfw")
    d.crawl("https://reddtastic.com/r/pics+earthporn", "sfw")
