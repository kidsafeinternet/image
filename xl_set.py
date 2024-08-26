from set_creation import dataset

if __name__ == '__main__':
    d = dataset("xl_set", 10000)
    d.crawl("https://reddtastic.com/r/nsfw+gonewild+gonewild18+18_19+boobs+pussy+penis?sort=new", "nsfw")
    d.crawl("https://reddtastic.com/r/pics+earthporn+programmerhumor+pictures+dogs+cats?sort=new", "sfw")