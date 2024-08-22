from set_creation import dataset

if __name__ == '__main__':
    d = dataset("medium_set", 100)
    d.crawl("https://reddtastic.com/r/nsfw", "nsfw")
    d.crawl("https://reddtastic.com/r/pics+earthporn", "sfw")