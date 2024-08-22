from set_creation import dataset

if __name__ == '__main__':
    d = dataset("large_set", 500)
    d.crawl("https://reddtastic.com/r/nsfw+gonewild+18_19?sort=new", "nsfw")
    d.crawl("https://reddtastic.com/r/pics+earthporn+programmerhumor?sort=new", "sfw")