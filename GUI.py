from web_scraping import CoursePage
if __name__ == '__main__':
    cp = CoursePage("2019","92","34190")
    print(cp.get_status())
