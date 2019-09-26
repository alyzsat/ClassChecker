from web_scraping import CoursePage
if __name__ == '__main__':
    cp = CoursePage("2019", "92", "34414")
    cp.refresh()
    print(cp.get_restrictions())
